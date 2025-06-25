import os
from datetime import datetime
from notion_poller import database_handler as db
from common import notion_handler as notion
from common import gpt_handler as gpt

DATABASE_ID = os.getenv("NOTION_DATABASE_ID")

def poll_notion():
    pages = notion.get_pages_and_update_times() # returns list of page ids
    # pages = [("1f5633fa-e4f4-80e0-a86f-c390eaaaa0fe", "2024-01-01")]
    print(f"Polling {len(pages)} pages")
    for page_id, date_updated, name in pages:
        last_updated = db.get_page_date_updated(page_id)
        if last_updated is None or last_updated < date_updated: # Page has been updated since last check or doesn't exist in DB 
            try:
                notes = notion.get_page_notes(page_id)
                if not notes:
                    print(f"No notes found for page: {name}")
                    continue
                
                print(f"Formatting notes for page: {name}")
                formatted = gpt.generate_response(notes)
                notion.update_page_formatted_notes(page_id, formatted)

                current_date = datetime.now().strftime("%Y-%d-%m")

                if last_updated is None:
                    print(f"Page {name} doesn't exist in DB, adding it")
                    db.add_page(page_id, current_date)
                else:
                    db.update_page_date_updated(page_id, current_date)
            except Exception as e:
                print(f"Error processing page {name}: {e}")
        else:
            print(f"Page {name} has not been updated since last check")
    print("Polling complete")

if __name__ == "__main__":
    poll_notion()
