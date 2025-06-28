import os
from datetime import datetime
from notion_poller import database_handler as db
from common import notion_handler as notion
from common import gpt_handler as gpt

DATABASE_ID = os.getenv("NOTION_DATABASE_ID")

def poll_notion():
    pages = notion.get_pages_and_update_times() # returns list of page ids
    print(f"Polling {len(pages)} pages")
    for page_id, date_updated, name in pages:
        last_updated = db.get_page_date_updated(page_id) 
        date_updated = datetime.strptime(date_updated[:10], "%Y-%m-%d")
        date_updated = date_updated.strftime("%Y-%m-%d")
        if last_updated is None or last_updated < date_updated: # Page has been updated since last check or doesn't exist in DB 
            try:
                notes = notion.get_page_notes(page_id)
                if not notes:
                    print(f"No notes found for page: {name}")
                    continue
                
                print(f"Formatting notes for page: {name}")
                formatted = gpt.generate_response(notes)
                notion.update_page_formatted_notes(page_id, formatted)

                current_date = str(datetime.now().strftime("%Y-%m-%d"))

                if last_updated is None:
                    print(f"Page {name} doesn't exist in DB, adding it")
                    db.add_page(page_id, current_date, name)
                else:
                    db.update_page_date_updated(page_id, current_date)
            except Exception as e:
                print(f"Error processing page {name}: {e}")
        else:
            print(f"Page {name} has not been updated since last check")
    print("Polling complete")

if __name__ == "__main__":
    poll_notion()
