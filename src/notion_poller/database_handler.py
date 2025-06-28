from supabase import create_client, Client
import os
from dotenv import load_dotenv

load_dotenv()

PSQL_URL = os.environ.get("PSQL_URL")
PSQL_KEY = os.environ.get("PSQL_KEY")
DB_NAME = "page"

def get_connection():
    supabase: Client = create_client(PSQL_URL, PSQL_KEY)
    return supabase

def add_page(page_id, date_updated, name):
    conn = get_connection()
    conn.table(DB_NAME).insert({"id": page_id, "date_updated": date_updated, "name": name}).execute()

def get_page_date_updated(page_id):
    conn = get_connection()
    result = conn.table(DB_NAME).select("date_updated").eq("id", page_id).execute()
    return result.data[0]["date_updated"] if result.data else None

def update_page_date_updated(page_id, date_updated):
    conn = get_connection()
    conn.table(DB_NAME).update({"date_updated": date_updated}).eq("id", page_id).execute()