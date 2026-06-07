# data_loader.py
import pandas as pd

REQUIRED_COLUMNS = [
    "full_name",
    "designation",
    "company_name",
    "industry",
    "country",
    "company_size",
    "engagement"
]

OPTIONAL_COLUMNS = [
    "linkedin_profile",
    "work_email",
    "phone_number",
    "website"
]

HEADER_ALIASES = {
    "full_name": ["full_name", "name", "contact_name", "lead_name"],
    "designation": ["designation", "role", "title", "position"],
    "company_name": ["company_name", "company", "organization", "org", "company_name"],
    "industry": ["industry"],
    "country": ["country", "location"],
    "linkedin_profile": ["linkedin_profile", "linkedin", "linkedin_url", "linkedin profile"],
    "work_email": ["work_email", "email", "email_address", "email address"],
    "phone_number": ["phone_number", "phone", "phone number", "mobile", "mobile_phone"],
    "website": ["website", "website_url", "url", "company_website", "website url"],
    "company_size": ["company_size", "size", "company size", "employees"],
    "engagement": ["engagement", "notes", "interaction", "activity"]
}


def normalize_key(key):
    if key is None:
        return ""
    return str(key).strip().lower().replace(" ", "_")


def safe_int(value, default=0):
    if value is None or value == "":
        return default
    if isinstance(value, (int, float)):
        return int(value)
    try:
        return int(str(value).strip())
    except (ValueError, TypeError):
        try:
            return int(float(str(value).strip()))
        except (ValueError, TypeError):
            return default


def normalize_text(value):
    if value is None:
        return ""
    return str(value).strip()


def build_column_map(columns):
    normalized_columns = {normalize_key(c): c for c in columns}
    mapped = {}

    for target, aliases in HEADER_ALIASES.items():
        for alias in aliases:
            normalized_alias = normalize_key(alias)
            if normalized_alias in normalized_columns:
                mapped[target] = normalized_columns[normalized_alias]
                break

    return mapped


def load_csv(file_path):
    df = pd.read_csv(file_path, dtype={"phone_number": str}, keep_default_na=False)
    df.columns = df.columns.str.strip()
    column_map = build_column_map(df.columns)

    missing = [col for col in REQUIRED_COLUMNS if col not in column_map]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    records = df.to_dict(orient="records")
    normalized = []

    for r in records:
        normalized_record = {
            "full_name": normalize_text(r.get(column_map.get("full_name"))),
            "designation": normalize_text(r.get(column_map.get("designation"))),
            "company_name": normalize_text(r.get(column_map.get("company_name"))),
            "industry": normalize_text(r.get(column_map.get("industry"))),
            "country": normalize_text(r.get(column_map.get("country"))),
            "linkedin_profile": normalize_text(r.get(column_map.get("linkedin_profile"))),
            "work_email": normalize_text(r.get(column_map.get("work_email"))),
            "phone_number": normalize_text(r.get(column_map.get("phone_number"))),
            "website": normalize_text(r.get(column_map.get("website"))),
            "company_size": safe_int(r.get(column_map.get("company_size"))),
            "engagement": normalize_text(r.get(column_map.get("engagement"))),
            "knowledge_base": "",
            "interaction_count": 0
        }
        normalized.append(normalized_record)

    return normalized
