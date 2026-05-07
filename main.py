from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from lead_qualifier import qualify_all_leads, score_lead, SAMPLE_LEADS

app = FastAPI()

leads_db = []

class NewLead(BaseModel):
    name: str
    role: str
    company: str
    industry: str
    country: str
    company_size: int
    engagement: str

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
    qualified = score_lead(new_lead)
    leads_db.append(qualified)
    return qualified

@app.delete("/api/leads/{index}")
def delete_lead(index: int):
    global leads_db
    if 0 <= index < len(leads_db):
        deleted = leads_db.pop(index)
        return {"message": f"Deleted {deleted['name']}"}
    return {"error": "Invalid index"}

@app.get("/", response_class=HTMLResponse)
def dashboard():
    with open("index.html", "r") as f:
        return f.read()