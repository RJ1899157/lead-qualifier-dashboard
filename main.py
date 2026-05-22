# main.py
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from lead_qualifier import qualify_all_leads, qualify_lead
from data_loader import load_csv
import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
import pandas as pd

load_dotenv()

app = FastAPI()
llm = ChatGroq(model="llama-3.3-70b-versatile", api_key=os.getenv("GROQ_API_KEY"))

leads_db = []

class NewLead(BaseModel):
    name: str
    role: str
    company: str
    industry: str
    country: str
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
    global leads_db
    if not leads_db:
        leads_db = qualify_all_leads()
    return leads_db

@app.post("/api/leads")
def add_lead(lead: NewLead):
    global leads_db
    new_lead = lead.dict()
    print(f"Qualifying new lead: {new_lead['name']}...")
    qualified = qualify_lead(new_lead)
    leads_db.append(qualified)
    return qualified

@app.post("/api/leads/upload-csv")
async def upload_csv(file: UploadFile = File(...)):
    global leads_db
    temp_path = f"temp_{file.filename}"

    with open(temp_path, "wb") as f:
        f.write(await file.read())

    records = load_csv(temp_path)
    added_count = 0
    replaced_count = 0

    for record in records:
        qualified = qualify_lead(record)

        duplicate_index = next(
            (i for i, existing in enumerate(leads_db)
             if existing["name"] == qualified["name"]
             and existing["company"] == qualified["company"]
            ),
            None
        )
        if duplicate_index is not None:
            leads_db[duplicate_index] = qualified
            replaced_count += 1
        else:
            leads_db.append(qualified)
            added_count += 1

    return {
        "message": "Upload complete",
        "added": added_count,
        "replaced": replaced_count
    }

@app.delete("/api/leads/{index}")
def delete_lead(index: int):
    global leads_db
    if 0 <= index < len(leads_db):
        deleted = leads_db.pop(index)
        return {"message": f"Deleted {deleted['name']}"}
    return {"error": "Invalid index"}

@app.get("/api/sales-assistant/{index}")
def get_sales_assistant(index: int):
    global leads_db
    if index < 0 or index >= len(leads_db):
        return {"error": "Invalid index"}
    lead = leads_db[index]

    discovery_prompt = f"""Generate 5 smart discovery questions to ask this lead in a sales call.
Lead: {lead['name']}, {lead['role']} at {lead['company']} ({lead['industry']}, {lead['country']}, {lead['company_size']} employees)
Engagement: {lead['engagement']}

Return ONLY a numbered list of 5 questions, nothing else."""

    pitch_prompt = f"""Generate a personalized sales pitch angle for this lead for an AI solutions company.
Lead: {lead['name']}, {lead['role']} at {lead['company']} ({lead['industry']}, {lead['country']}, {lead['company_size']} employees)
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

    return {
        "lead": lead,
        "discovery_questions": discovery,
        "pitch_suggestion": pitch
    }

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
    global chat_history, leads_db
    
    user_message = request.get("message", "")
    
    leads_context = "\n".join([
        f"- {l['name']} | {l['role']} at {l['company']} | {l['industry']} | {l['country']} | Score: {l.get('score', 'N/A')} | Status: {l.get('status', 'N/A')} | Engagement: {l['engagement']} | Reason: {l.get('reason', '')} | Action: {l.get('action', '')}"
        for l in leads_db
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
    
    return {"response": response.content}

@app.post("/api/chat/reset")
def reset_chat():
    global chat_history
    chat_history = []
    return {"message": "Chat reset"}

@app.get("/", response_class=HTMLResponse)
def dashboard():
    with open("index.html", "r") as f:
        return f.read()

@app.get("/sales-assistant", response_class=HTMLResponse)
def sales_assistant_page():
    with open("sales_assistant.html", "r") as f:
        return f.read()