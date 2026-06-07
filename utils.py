#utils.py
import uuid

def generate_lead_id():
    return f"lead_{uuid.uuid4().hex[:8]}"