# main.py
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel
from lead_qualifier import qualify_lead
from data_loader import load_csv
import os
import tempfile
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from lead_repository import get_all_leads, create_lead, update_lead, delete_lead
from utils import generate_lead_id

load_dotenv()

app = FastAPI()
llm = ChatGroq(model="llama-3.3-70b-versatile", api_key=os.getenv("GROQ_API_KEY"))

def json_response(content):
    return JSONResponse(content=content, media_type="application/json; charset=utf-8")

class NewLead(BaseModel):
    full_name: str
    designation: str
    company_name: str
    industry: str
    country: str
    linkedin_profile: str = ""
    work_email: str = ""
    phone_number: str = ""
    website: str = ""
    company_size: int
    engagement: str

class MeetingSummary(BaseModel):
    lead_name: str
    lead_role: str
    lead_company: str
    lead_industry: str
    notes: str

@app.get("/api/leads")
def get_leads():
    return json_response(get_all_leads())

@app.post("/api/leads")
def add_lead(lead: NewLead):
    new_lead = lead.dict()
    qualified = qualify_lead(new_lead)
    qualified["lead_id"] = generate_lead_id()
    created = create_lead(qualified)
    qualified["_record_id"] = created["id"]
    return json_response(qualified)


@app.post("/api/leads/upload-csv")
async def upload_csv(file: UploadFile = File(...)):
    existing_leads = get_all_leads()
    temp_path = None

    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as temp_file:
            temp_file.write(await file.read())
            temp_path = temp_file.name

        records = load_csv(temp_path)
        added_count = 0
        replaced_count = 0

        for record in records:
            qualified = qualify_lead(record)
            duplicate = next(
                (
                    lead for lead in existing_leads
                    if lead["full_name"] == qualified["full_name"]
                    and lead["company_name"] == qualified["company_name"]
                ),
                None
            )

            if duplicate is not None:
                qualified["lead_id"] = duplicate["lead_id"]
                update_lead(duplicate["_record_id"], qualified)
                duplicate.update(qualified)
                replaced_count += 1
            else:
                qualified["lead_id"] = generate_lead_id()
                created = create_lead(qualified)
                qualified["_record_id"] = created["id"]
                existing_leads.append(qualified)
                added_count += 1

        return json_response({
            "message": "Upload complete",
            "added": added_count,
            "replaced": replaced_count
        })
    except ValueError as exc:
        return JSONResponse(
            status_code=400,
            content={"error": str(exc)},
            media_type="application/json; charset=utf-8"
        )
    except Exception as exc:
        return JSONResponse(
            status_code=500,
            content={"error": "Unable to process CSV upload. " + str(exc)},
            media_type="application/json; charset=utf-8"
        )
    finally:
        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)

@app.delete("/api/leads/{record_id}")
def delete_lead_endpoint(record_id: str):
    delete_lead(record_id)
    return json_response({"message": "Lead deleted"})

@app.put("/api/leads/{record_id}")
def update_lead_endpoint(record_id: str, lead: NewLead):
    updated = lead.dict()
    qualified = qualify_lead(updated)
    existing_leads = get_all_leads()
    existing = next((l for l in existing_leads if l["_record_id"] == record_id), None)
    qualified["lead_id"] = existing["lead_id"] if existing else generate_lead_id()
    update_lead(record_id, qualified)
    qualified["_record_id"] = record_id
    return json_response(qualified)

@app.get("/api/sales-assistant/{index}")
def get_sales_assistant(index: int):
    leads = get_all_leads()
    if index < 0 or index >= len(leads):
        return {"error": "Invalid index"}
    lead = leads[index]

    discovery_prompt = f"""Generate 5 smart discovery questions to ask this lead in a sales call.
Lead: {lead['full_name']}, {lead['designation']} at {lead['company_name']} ({lead['industry']}, {lead['country']}, {lead['company_size']} employees)
Engagement: {lead['engagement']}

Return ONLY a numbered list of 5 questions, nothing else."""

    pitch_prompt = f"""Generate a personalized sales pitch angle for this lead for an AI solutions company.
Lead: {lead['full_name']}, {lead['designation']} at {lead['company_name']} ({lead['industry']}, {lead['country']}, {lead['company_size']} employees)
Engagement: {lead['engagement']}
Lead Status: {lead.get('status')}

Return ONLY the pitch in 3-4 sentences, nothing else."""

    discovery = llm.invoke([
        SystemMessage(content="You are a sales expert. Return only what is asked, no extra text."),
        HumanMessage(content=discovery_prompt)
    ]).content

    pitch = llm.invoke([
        SystemMessage(content="You are a sales expert. Return only what is asked, no extra text."),
        HumanMessage(content=pitch_prompt)
    ]).content

    return json_response({"lead": lead, "discovery_questions": discovery, "pitch_suggestion": pitch})

@app.post("/api/meeting-summary")
def generate_meeting_summary(data: MeetingSummary):
    prompt = f"""Generate a professional meeting summary based on these notes.
Lead: {data.lead_name}, {data.lead_role} at {data.lead_company} ({data.lead_industry})
Meeting Notes: {data.notes}

Return a structured summary with:
SUMMARY: (2-3 sentences)
KEY POINTS: (3 bullet points)
NEXT STEPS: (2 action items)"""

    response = llm.invoke([
        SystemMessage(content="You are a sales assistant. Generate professional meeting summaries."),
        HumanMessage(content=prompt)
    ]).content

    return {"summary": response}

chat_history = []

@app.post("/api/chat")
def chat_with_leads(request: dict):
    global chat_history
    leads = get_all_leads()
    
    user_message = request.get("message", "")
    
    leads_context = "\n".join([
        f"- {l['full_name']} | {l['designation']} at {l['company_name']} | {l['industry']} | {l['country']} | Score: {l.get('score', 'N/A')} | Status: {l.get('status', 'N/A')} | Engagement: {l['engagement']} | Reason: {l.get('score_explanation', '')} | Action: {l.get('recommended_action', '')}"
        for l in leads
    ])
    
    if not chat_history:
        chat_history.append(SystemMessage(content=f"""You are an AI sales assistant with full knowledge of the current lead database. 
Help the sales team by answering questions about leads, suggesting outreach strategies, drafting emails, and providing sales intelligence.

Current Lead Database:
{leads_context}

You can:
- Summarize any lead's profile
- Recommend which leads to contact first
- Draft personalized emails
- Suggest conversation starters
- Answer any question about the leads
- Provide sales strategy advice

Always be concise, actionable and specific to the leads in the database."""))
    
    chat_history.append(HumanMessage(content=user_message))
    response = llm.invoke(chat_history)
    chat_history.append(AIMessage(content=response.content))
    
    return json_response({"response": response.content})

@app.post("/api/chat/reset")
def reset_chat():
    global chat_history
    chat_history = []
    return json_response({"message": "Chat reset"})

@app.get("/", response_class=HTMLResponse)
def dashboard():
    with open("index.html", "r", encoding="utf-8") as f:
        return f.read()

@app.get("/sales-assistant", response_class=HTMLResponse)
def sales_assistant_page():
    with open("sales_assistant.html", "r", encoding="utf-8") as f:
        return f.read()

@app.get("/sales-assistant/", response_class=HTMLResponse)
def sales_assistant_page_slash():
    return sales_assistant_page()

@app.get("/sales_assistant.html", response_class=HTMLResponse)
def sales_assistant_file():
    return sales_assistant_page()
