# lead_qualifier.py

import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage
from scoring import score_lead_deterministic

load_dotenv()

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    api_key=os.getenv("GROQ_API_KEY")
)

def generate_reason_and_action(lead):
    prompt = f"""
You are a sales intelligence assistant.
A deterministic scoring engine has already scored this lead.
Your task is ONLY to explain the score in human-readable form.

Lead Details:
- Name: {lead['full_name']}
- Role: {lead['designation']}
- Company: {lead['company_name']}
- Industry: {lead['industry']}
- Country: {lead['country']}
- Company Size: {lead['company_size']}
- Engagement: {lead['engagement']}

Final Score: {lead['score']}
Final Status: {lead['status']}

Scoring Breakdown:
- Role Score: {lead['score_breakdown']['role_score']}
- Industry Score: {lead['score_breakdown']['industry_score']}
- Country Score: {lead['score_breakdown']['country_score']}
- Company Size Score: {lead['score_breakdown']['company_size_score']}
- Engagement Score: {lead['score_breakdown']['engagement_score']}

Explain:
1. Which factors contributed most to the score
2. Why this lead received its status
3. Recommended next action

Return ONLY:

REASON: concise explanation
ACTION: concise action
"""

    try:
        response = llm.invoke([
            SystemMessage(content="You are a sales assistant."),
            HumanMessage(content=prompt)
        ]).content
        return parse_response(response)

    except Exception as e:
        print("LLM ERROR:", e)
        return {
            "reason": "Lead scored using deterministic scoring engine.",
            "action": "Review lead manually for next steps."
        }

def parse_response(response):
    result = {}

    for line in response.split("\n"):
        if line.startswith("REASON:"):
            result["reason"] = line.replace("REASON:", "").strip()

        elif line.startswith("ACTION:"):
            result["action"] = line.replace("ACTION:", "").strip()

    return result

def qualify_lead(lead):
    scored = score_lead_deterministic(lead)
    ai_result = generate_reason_and_action(scored)
    scored["score_explanation"] = ai_result.get("reason", "Lead scored using deterministic scoring.")
    scored["recommended_action"] = ai_result.get("action", "Review lead manually.")
    return scored

def qualify_all_leads():
    return []