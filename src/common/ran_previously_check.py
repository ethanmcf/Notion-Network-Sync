import sys
from supabase import create_client, Client
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

load_dotenv()

PSQL_URL = os.environ.get("PSQL_URL")
PSQL_KEY = os.environ.get("PSQL_KEY")
DB_NAME = "servicerun"

def get_connection():
    supabase: Client = create_client(PSQL_URL, PSQL_KEY)
    return supabase

def should_exit(service_name):
    conn = get_connection()
    result = conn.table(DB_NAME).select("last_run").eq("service_name", service_name).execute()
    days_ago = (datetime.now() - timedelta(days=2)).strftime("%Y-%m-%d")
    if not result.data or result.data[0]["last_run"] < days_ago:
        now = datetime.now().strftime("%Y-%m-%d")
        if not result.data:
            conn.table(DB_NAME).insert({"service_name": service_name, "last_run": now}).execute()
        else:
            conn.table(DB_NAME).update({"last_run": now}).eq("service_name", service_name).execute()
        sys.exit(1)
    else:
        print(f"Service {service_name} has run recently at {result.data[0]['last_run']}")
        sys.exit(0)

if __name__ == "__main__":
    service_name = sys.argv[1]
    print(f"Checking if {service_name} has run recently")
    should_exit(service_name)