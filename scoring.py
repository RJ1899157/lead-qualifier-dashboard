# scoring.py

ROLE_SCORES = {
    "CEO": 30,
    "Founder": 30,
    "CTO": 25,
    "VP Marketing": 25,
    "Director": 20,
    "Manager": 10,
    "Junior Manager": 5
}

INDUSTRY_SCORES = {
    "EdTech": 25,
    "Pharma": 25,
    "Retail": 20,
    "Media": 18,
    "Real Estate": 15
}

COUNTRY_SCORES = {
    "USA": 15,
    "Canada": 12,
    "Singapore": 10,
    "UAE": 10,
    "India": 5
}


def get_company_size_score(size):
    if size >= 500:
        return 20
    elif size >= 100:
        return 15
    elif size >= 20:
        return 10
    return 5


def get_engagement_score(engagement):
    engagement = engagement.lower()

    if "requested" in engagement or "demo" in engagement or "call" in engagement:
        return 10

    if "replied" in engagement:
        return 8

    if "opened" in engagement or "clicked" in engagement:
        return 5

    return 0


def classify_lead(score):
    # Align status boundaries with frontend score coloring and reserve Hot for the top tier.
    if score >= 80:
        return "Hot"
    elif score >= 50:
        return "Warm"
    return "Cold"


def score_lead_deterministic(lead):
    role_score = ROLE_SCORES.get(lead["role"], 5)
    industry_score = INDUSTRY_SCORES.get(lead["industry"], 10)
    country_score = COUNTRY_SCORES.get(lead["country"], 5)
    company_size_score = get_company_size_score(lead["company_size"])
    engagement_score = get_engagement_score(lead["engagement"])

    total_score = (
        role_score +
        industry_score +
        country_score +
        company_size_score +
        engagement_score
    )

    status = classify_lead(total_score)

    explanation = {
        "role_score": role_score,
        "industry_score": industry_score,
        "country_score": country_score,
        "company_size_score": company_size_score,
        "engagement_score": engagement_score
    }

    return {
        **lead,
        "score": total_score,
        "status": status,
        "score_breakdown": explanation
    }