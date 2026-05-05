import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage

load_dotenv()

llm = ChatGroq(model="llama-3.3-70b-versatile", api_key=os.getenv("GROQ_API_KEY"))

SAMPLE_LEADS = [
    {"name": "John Smith", "role": "CEO", "company": "EduTech Pro", "industry": "EdTech", "country": "USA", "company_size": 250, "engagement": "Opened email 3 times, replied once"},
    {"name": "Sarah Chen", "role": "CTO", "company": "PharmaAI", "industry": "Pharma", "country": "Canada", "company_size": 500, "engagement": "Visited website twice"},
    {"name": "Raj Patel", "role": "Founder", "company": "RetailX", "industry": "Retail", "country": "Singapore", "company_size": 80, "engagement": "No engagement"},
    {"name": "Emily Davis", "role": "VP Marketing", "company": "MediaCorp", "industry": "Media", "country": "USA", "company_size": 1200, "engagement": "Replied to email, asked for demo"},
    {"name": "Ahmed Hassan", "role": "Director", "company": "RealEstate Plus", "industry": "Real Estate", "country": "UAE", "company_size": 150, "engagement": "Opened email once"},
    {"name": "Lisa Wong", "role": "Junior Manager", "company": "SmallShop", "industry": "Retail", "country": "India", "company_size": 12, "engagement": "No engagement"},
    {"name": "Mark Johnson", "role": "Founder", "company": "EduStart", "industry": "EdTech", "country": "Canada", "company_size": 45, "engagement": "Opened email twice, clicked link"},
    {"name": "Priya Sharma", "role": "CEO", "company": "PharmaGlobal", "industry": "Pharma", "country": "Singapore", "company_size": 800, "engagement": "Requested a call"}
]

def score_lead(lead):
    prompt = f"""
You are a lead qualification expert for an AI solutions company targeting decision-makers in EdTech, Pharma, Retail, Real Estate and Media in USA, Canada, Singapore and Middle East.

Analyze this lead and respond in EXACTLY this format with no extra text:
STATUS: [Hot/Warm/Cold]
SCORE: [0-100]
REASON: [one sentence explanation]
ACTION: [one specific recommended action]

Lead details:
- Name: {lead['name']}
- Role: {lead['role']}
- Company: {lead['company']}
- Industry: {lead['industry']}
- Country: {lead['country']}
- Company Size: {lead['company_size']} employees
- Engagement: {lead['engagement']}
"""
    messages = [
        SystemMessage(content="You are a lead qualification expert. Always respond in the exact format requested."),
        HumanMessage(content=prompt)
    ]
    response = llm.invoke(messages)
    return parse_response(response.content, lead)

def parse_response(response, lead):
    lines = response.strip().split('\n')
    result = lead.copy()
    for line in lines:
        if line.startswith("STATUS:"):
            result["status"] = line.replace("STATUS:", "").strip()
        elif line.startswith("SCORE:"):
            result["score"] = line.replace("SCORE:", "").strip()
        elif line.startswith("REASON:"):
            result["reason"] = line.replace("REASON:", "").strip()
        elif line.startswith("ACTION:"):
            result["action"] = line.replace("ACTION:", "").strip()
    return result

def qualify_all_leads():
    results = []
    for lead in SAMPLE_LEADS:
        print(f"Analyzing {lead['name']}...")
        result = score_lead(lead)
        results.append(result)
    return results

if __name__ == "__main__":
    results = qualify_all_leads()
    print("\n" + "="*60)
    for r in results:
        print(f"\n{r['name']} | {r['role']} at {r['company']}")
        print(f"Status: {r.get('status')} | Score: {r.get('score')}")
        print(f"Reason: {r.get('reason')}")
        print(f"Action: {r.get('action')}")