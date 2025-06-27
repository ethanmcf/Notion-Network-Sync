import psycopg2

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
                CREATE TABLE IF NOT EXISTS page (
                    id TEXT PRIMARY KEY,
                    date_updated TIMESTAMP NOT NULL
                )
        """)
        conn.commit()

def add_page(page_id, date_updated):
    create_table()
    with get_connection() as conn:
        c = conn.cursor()
        c.execute("INSERT INTO page (id, date_updated) VALUES (%s, %s)", (page_id, date_updated))
        conn.commit()

def get_page_date_updated(page_id):
    create_table()
    with get_connection() as conn:
        c = conn.cursor()
        c.execute("SELECT date_updated FROM page WHERE id = %s", (page_id,))
        result = c.fetchone()
        return result[0] if result else None

def update_page_date_updated(page_id, date_updated):
    create_table()
    with get_connection() as conn:
        c = conn.cursor()
        c.execute("UPDATE page SET date_updated = %s WHERE id = %s", (date_updated, page_id))
        conn.commit()