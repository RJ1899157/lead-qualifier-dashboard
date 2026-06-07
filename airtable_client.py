#airtable_client.py
import os
from dotenv import load_dotenv
from pyairtable import Api

load_dotenv()

api = Api(os.getenv("AIRTABLE_TOKEN"))

base = api.base(
    os.getenv("AIRTABLE_BASE_ID")
)

leads_table = base.table("Leads")