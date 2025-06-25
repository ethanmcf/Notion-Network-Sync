from linkedin_scraper import linkedin_handler as lh
from common import notion_handler as nh

def scrape():
    contacts = lh.get_recent_contacts()

    nh.add_contacts_to_notion(contacts)

if __name__ == "__main__":
    scrape() 