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
                CREATE TABLE IF NOT EXISTS contact (
                    name TEXT PRIMARY KEY,
                    date_updated TIMESTAMP NOT NULL
                )
        """)
        conn.commit()

def add_contact(name, date_updated):
    create_table()
    with get_connection() as conn:
        c = conn.cursor()
        c.execute("INSERT INTO contact (name, date_updated) VALUES (%s, %s)", (name, date_updated))
        conn.commit()

def get_contact_date_updated(name):
    create_table()
    with get_connection() as conn:
        c = conn.cursor()
        c.execute("SELECT date_updated FROM contact WHERE name = %s", (name,))
        result = c.fetchone()
        return result[0] if result else None

def update_page_date_updated(name, date_updated):
    create_table()
    with get_connection() as conn:
        c = conn.cursor()
        c.execute("UPDATE contact SET date_updated = %s WHERE name = %s", (date_updated, name))
        conn.commit()