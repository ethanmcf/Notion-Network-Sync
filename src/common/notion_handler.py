import os
from notion_client import Client
from dotenv import load_dotenv

load_dotenv()

NOTION_API_KEY = os.getenv("NOTION_API_KEY")
DATABASE_ID = os.getenv("NOTION_DATABASE_ID")

notion = Client(auth=NOTION_API_KEY)

def _parse_notion_contact(page_json):
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
        "LinkedIn URL": page_json.get("url")
    }
    # TODO: Add formatted notes and personal notes, email, phone, 
    return name, info

def _create_heading_block(text, level=2):
    block_type = f"heading_{level}"
    return {
        "object": "block",
        "type": block_type,
        block_type: {
            "rich_text": [{"type": "text", "text": {"content": text}}]
        },
    }

def _create_paragraph_block(text, link=None):
    text_obj = {"type": "text", "text": {"content": text}}
    if link:
        text_obj["text"]["link"] = {"url": link}
    return {
        "object": "block",
        "type": "paragraph",
        "paragraph": {"rich_text": [text_obj]},
    }

def get_contacts_from_notion():
        contacts = {}
        for entry in notion.databases.query(DATABASE_ID)["results"]:
            name, info = _parse_notion_contact(entry)
            contacts[name] = info
        return contacts

def create_contact_page(contact):
    email = contact.get("Email", "")
    phone = contact.get("Phone", "")
    linkedin_url = contact.get("LinkedIn URL", "")
    formatted_notes = contact.get("Formatted Notes", "")
    personal_notes = contact.get("Personal Notes", "")

    children = [
        _create_heading_block("Email"),
        _create_paragraph_block(email),

        _create_heading_block("Phone"),
        _create_paragraph_block(phone),

        _create_heading_block("Linkedin"),
        _create_paragraph_block(linkedin_url, link=linkedin_url),

        _create_heading_block("Personal Notes"),
        _create_paragraph_block(personal_notes),
        
        _create_heading_block("Formatted Notes"),
        _create_paragraph_block(formatted_notes),
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

def get_page_notes(page_id):
    blocks = notion.blocks.children.list(page_id)["results"]
    notes = []
    capture = False
    for block in blocks:
        if (
            block["type"] == "heading_2" and \
            len(block["heading_2"]["rich_text"]) > 0 and \
            "Formatted Notes" in block["heading_2"]["rich_text"][0]["text"]["content"]
        ):

            capture = True
            continue
        if capture and block["type"] == "paragraph":
            text = block["paragraph"]["rich_text"]
            if text:
                notes.append(text[0]["text"]["content"])
    return "\n".join(notes)

def update_page_formatted_notes(page_id, formatted_notes):
    # Clear formated notes
    blocks = notion.blocks.children.list(page_id)["results"]
    capture = False
    for block in blocks:
        if (
            block["type"] == "heading_2" and \
            len(block["heading_2"]["rich_text"]) > 0 and \
            "Formatted Notes" in block["heading_2"]["rich_text"][0]["text"]["content"]
        ):
            capture = True
            continue
        if capture and block["type"] == "paragraph":
            notion.blocks.delete(block["id"])
    
    # Add new formatted notes
    children = [
        _create_paragraph_block(formatted_notes)
    ]
    notion.blocks.children.append(page_id, children=children)

def get_pages_and_update_times():
    pages = []
    for entry in notion.databases.query(database_id=DATABASE_ID)["results"]:
        page_id = entry["id"]
        date_updated = entry["last_edited_time"]
        name = entry["properties"]["Name"]["title"][0]["plain_text"]
        pages.append((page_id, date_updated, name))
    return pages

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