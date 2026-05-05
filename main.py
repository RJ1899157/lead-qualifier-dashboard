from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from lead_qualifier import qualify_all_leads

app = FastAPI()

@app.get("/api/leads")
def get_leads():
    return qualify_all_leads()

@app.get("/", response_class=HTMLResponse)
def dashboard():
    with open("index.html", "r") as f:
        return f.read()