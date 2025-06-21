from linkedin_scraper import get_recent_contacts
from notion_handler import add_contacts_to_notion

def main():
    contacts = get_recent_contacts()
    # contacts = [{'Name': 'Danielle Sacks', 'Company': 'John Howard Society of Ontario', 'LinkedIn URL': 'https://www.linkedin.com/in/ACoAAEgFDWsBsrH0ofD2JcQYI7G1mCEZadSSK6g', 'Date Messaged': '2025-06-20'}, {'Name': 'Osama Saleh', 'Company': 'LinkedIn', 'LinkedIn URL': 'https://www.linkedin.com/in/ACoAABzhoBABqIgmHo2YYmPyxwgxtb8NCgTo5sc', 'Date Messaged': '2025-06-20'}]
    add_contacts_to_notion(contacts)

if __name__ == "__main__":
    main() 