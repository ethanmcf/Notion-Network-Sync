from linkedin_scraper.linkedin_handler import get_recent_contacts
from common.notion_handler import add_contacts_to_notion
# from common.gpt_handler import generate_response

def main():
    contacts = get_recent_contacts()
    add_contacts_to_notion(contacts)

if __name__ == "__main__":
    main() 