import sys
import psycopg2
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_PATH = os.getenv("PSQL_DATABASE_PATH")

def get_connection():
    return psycopg2.connect(DATABASE_PATH)

def create_table():
    with get_connection() as conn:
        c = conn.cursor()
        c.execute("""
                CREATE TABLE IF NOT EXISTS runs (
                    service_name TEXT PRIMARY KEY,
                    last_run TIMESTAMP NOT NULL
                )
        """)
        conn.commit()

def should_exit(service_name):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT lastrun FROM runs WHERE service_name = %s",
                (service_name,)
            )
            result = cur.fetchone()
            if result is None or result[0] < datetime.now() - timedelta(days=2):
                # No record for service_name, exit 0
                print(f"No record for service '{service_name}'. Exiting with code 0.")
                sys.exit(0)

            # Update lastrun to current time
            now = datetime.now()
            cur.execute(
                "UPDATE runs SET lastrun = %s WHERE service_name = %s",
                (now, service_name)
            )
            conn.commit()
            print(f"Updated lastrun to {now} for service '{service_name}'")
            sys.exit(1)

if __name__ == "__main__":
    service_name = sys.argv[1]
    create_table()
    should_exit(service_name)