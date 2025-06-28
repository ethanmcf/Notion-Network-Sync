from supabase import create_client, Client
import os
from dotenv import load_dotenv

load_dotenv()

PSQL_URL = os.environ.get("PSQL_URL")
PSQL_KEY = os.environ.get("PSQL_KEY")
DB_NAME = "contact"

def get_connection():
    supabase: Client = create_client(PSQL_URL, PSQL_KEY)
    return supabase

def add_contact(name, date_updated):
    conn = get_connection()
    conn.table(DB_NAME).insert({"name": name, "date_updated": date_updated}).execute()

def get_contact_date_updated(name):
    conn = get_connection()
    result = conn.table(DB_NAME).select("date_updated").eq("name", name).execute()
    return result.data[0]["date_updated"] if result.data else None

def update_page_date_updated(name, date_updated):
    conn = get_connection()
    conn.table(DB_NAME).update({"date_updated": date_updated}).eq("name", name).execute()