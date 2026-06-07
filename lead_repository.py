#lead_repository.py
from airtable_client import leads_table


def get_all_leads():
    records = leads_table.all()
    result = []

    for record in records:
        f = record["fields"]
        result.append({
            "_record_id": record["id"],
            "lead_id": f.get("lead_id"),
            "full_name": f.get("full_name"),
            "designation": f.get("designation"),
            "company_name": f.get("company_name"),
            "industry": f.get("industry"),
            "country": f.get("country"),
            "linkedin_profile": f.get("linkedin_profile"),
            "work_email": f.get("work_email"),
            "phone_number": f.get("phone_number"),
            "website": f.get("website"),
            "company_size": f.get("company_size"),
            "score": f.get("score"),
            "status": f.get("status"),
            "priority_rank": f.get("priority_rank"),
            "score_explanation": f.get("score_explanation", ""),
            "recommended_action": f.get("recommended_action", ""),
            "ai_summary": f.get("ai_summary", ""),
            "engagement": f.get("engagement", ""),
            "interaction_count": f.get("interaction_count", 0)
        })
    return result


def _to_airtable_fields(lead):
    return {
        "lead_id": lead.get("lead_id"),
        "full_name": lead.get("full_name"),
        "designation": lead.get("designation"),
        "company_name": lead.get("company_name"),
        "industry": lead.get("industry"),
        "country": lead.get("country"),
        "linkedin_profile": lead.get("linkedin_profile", ""),
        "work_email": lead.get("work_email", ""),
        "phone_number": lead.get("phone_number", ""),
        "website": lead.get("website", ""),
        "company_size": lead.get("company_size"),
        "engagement": lead.get("engagement", ""),
        "score": lead.get("score"),
        "status": lead.get("status"),
        "score_explanation": lead.get("score_explanation", ""),
        "recommended_action": lead.get("recommended_action", ""),
        "ai_summary": lead.get("ai_summary", ""),
        "interaction_count": lead.get("interaction_count", 0),
        "knowledge_base": str(lead.get("knowledge_base", "")),
        "priority_rank": lead.get("priority_rank", 0)
    }


def create_lead(lead):
    return leads_table.create(_to_airtable_fields(lead))


def update_lead(record_id, lead):
    return leads_table.update(record_id, _to_airtable_fields(lead))


def delete_lead(record_id):
    leads_table.delete(record_id)
