from linkedin_scraper import get_recent_contacts
# from notion_client import add_contacts_to_notion

def main():
    contacts = get_recent_contacts()
    # add_contacts_to_notion(contacts)

if __name__ == "__main__":
    main() 