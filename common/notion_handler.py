import os
from notion_client import Client
from dotenv import load_dotenv

load_dotenv()

NOTION_API_KEY = os.getenv("NOTION_API_KEY")
DATABASE_ID = os.getenv("DATABASE_ID")

notion = Client(auth=NOTION_API_KEY)

def parse_notion_contact(page_json):
    props = page_json.get("properties", {})

    def extract_title(prop):
        return prop["title"][0]["plain_text"] if prop.get("title") else None

    def extract_rich_text(prop):
        return prop["rich_text"][0]["plain_text"] if prop.get("rich_text") else None

    def extract_date(prop):
        return prop["date"]["start"] if prop.get("date") else None

    name = extract_title(props.get("Name", {}))
    info = {
        "Company": extract_rich_text(props.get("Company", {})),
        "Last Communicated": extract_date(props.get("Last Communicated", {})),
        "URL": page_json.get("url")
    }
    return name, info
    

def get_contacts_from_notion():
        contacts = {}
        for entry in notion.databases.query(DATABASE_ID)["results"]:
            name, info = parse_notion_contact(entry)
            contacts[name] = info
        return contacts

def create_heading_block(text, level=2):
    block_type = f"heading_{level}"
    return {
        "object": "block",
        "type": block_type,
        block_type: {
            "rich_text": [{"type": "text", "text": {"content": text}}]
        },
    }

def create_paragraph_block(text, link=None):
    text_obj = {"type": "text", "text": {"content": text}}
    if link:
        text_obj["text"]["link"] = {"url": link}
    return {
        "object": "block",
        "type": "paragraph",
        "paragraph": {"rich_text": [text_obj]},
    }

def create_contact_page(contact):
    email = contact.get("Email", "")
    phone = contact.get("Phone", "")
    linkedin_url = contact.get("LinkedIn URL", "")
    notes = contact.get("Notes", "")

    children = [
        create_heading_block("Email"),
        create_paragraph_block(email),

        create_heading_block("Phone"),
        create_paragraph_block(phone),

        create_heading_block("Linkedin"),
        create_paragraph_block(linkedin_url, link=linkedin_url),

        create_heading_block("Notes"),
        create_paragraph_block(notes),
    ]
    
    notion.pages.create(
        parent={"database_id": DATABASE_ID},
        properties={
            "Name": {"title": [{"text": {"content": contact["Name"]}}]},
            "Company": {"rich_text": [{"text": {"content": contact.get("Company", "")}}]},
            "Communicated On": {"multi_select": [{"name": "Linkedin"}]},
            "Last Communicated": {"date": {"start": contact.get("Date Messaged")}},
        },
        children=children,
    )

def update_contact_page(contact):
    page = notion.databases.query(
        database_id=DATABASE_ID,
        filter={
            "property": "Name",
            "title": {
                "equals": contact["Name"]
            }
        }
    )
    page_id = page.get("results", [])[0].get("id")

    notion.pages.update(
        page_id=page_id,
        properties={
            "Last Communicated": {"date": {"start": contact["Date Messaged"]}},
        },
    )
    
def add_contacts_to_notion(contacts):
    saved_contacts = get_contacts_from_notion()
    for contact in contacts:
        if contact["Name"] in saved_contacts:
            print(f"Contact: {contact['Name']} already exists...updating")
            try:
                update_contact_page(contact)
            except Exception as e:
                print(f"Failed to update contact {contact['Name']}: {e}") 

        else:
            print(f"Contact: {contact['Name']} does not exist...adding")
            try:
                create_contact_page(contact)
            except Exception as e:
                print(f"Failed to add contact {contact['Name']}: {e}") 