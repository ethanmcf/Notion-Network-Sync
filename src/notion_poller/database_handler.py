import sqlite3

DATABASE_NAME = "src/notion_poller/notion_data.db"

def get_connection():
    return sqlite3.connect(DATABASE_NAME)   

def create_table():
    with get_connection() as conn:
        c = conn.cursor()
        c.execute(
            """
            CREATE TABLE IF NOT EXISTS page (
                id TEXT PRIMARY KEY,
                date_updated TEXT NOT NULL
            )
            """
        )
        conn.commit()

def add_page(page_id, date_updated):
    with get_connection() as conn:
        c = conn.cursor()
        c.execute("INSERT INTO page (id, date_updated) VALUES (?, ?)", (page_id, date_updated))
        conn.commit()

def get_page_date_updated(page_id):
    with get_connection() as conn:
        c = conn.cursor()
        c.execute("SELECT date_updated FROM page WHERE id = ?", (page_id,))
        result = c.fetchone()
        return result[0] if result else None

def update_page_date_updated(page_id, date_updated):
    with get_connection() as conn:
        c = conn.cursor()
        c.execute("UPDATE page SET date_updated = ? WHERE id = ?", (date_updated, page_id))
        conn.commit()