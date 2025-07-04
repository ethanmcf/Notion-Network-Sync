import os
import re
from datetime import date
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright
from linkedin_scraper import database_handler as db

load_dotenv()

LINKEDIN_EMAIL = os.getenv("LINKEDIN_EMAIL")
LINKEDIN_PASSWORD = os.getenv("LINKEDIN_PASSWORD")
COOKIES_PATH = os.getenv("LINKEDIN_COOKIES_PATH")


def login(page):
    print("Not logged in, logging in...")
    page.goto("https://www.linkedin.com/login")

    print("Filling in email...")
    page.fill("#username", LINKEDIN_EMAIL)

    print("Filling in password...")
    page.fill("#password", LINKEDIN_PASSWORD)

    print("Clicking submit...")
    page.click("button[type=submit]")

    print("Waiting for page to load...")
    page.wait_for_load_state("load")

def parse_date_str(date_string):
    """
    Parse various date formats and return YYYY-MM-DD format for database.
    
    Handles:
    - Time only (10:00 PM) -> Today's date
    - Month Day (Sep 12) -> Current year
    - Full date (Sep 9, 2024) -> As is
    """
    
    # Remove extra whitespace and normalize
    date_string = date_string.strip()
    
    # Pattern 1: Time only (e.g., "10:00 PM", "2:30 AM")
    time_pattern = r'^(\d{1,2}):(\d{2})\s*(AM|PM)$'
    time_match = re.match(time_pattern, date_string)
    if time_match:
        return date.today().strftime('%Y-%m-%d')
    
    # Pattern 2: Month Day (e.g., "Sep 12", "Dec 3")
    month_day_pattern = r'^(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+(\d{1,2})$'
    month_day_match = re.match(month_day_pattern, date_string, re.IGNORECASE)
    if month_day_match:
        month_name = month_day_match.group(1)
        day = month_day_match.group(2)
        current_year = date.today().year
        
        # Convert month abbreviation to number
        month_map = {
            'jan': 1, 'feb': 2, 'mar': 3, 'apr': 4, 'may': 5, 'jun': 6,
            'jul': 7, 'aug': 8, 'sep': 9, 'oct': 10, 'nov': 11, 'dec': 12
        }
        
        month_num = month_map[month_name.lower()]
        return f"{current_year}-{month_num:02d}-{int(day):02d}"
    
    # Pattern 3: Full date (e.g., "Sep 9, 2024", "Dec 3, 2024")
    full_date_pattern = r'^(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+(\d{1,2}),\s+(\d{4})$'
    full_date_match = re.match(full_date_pattern, date_string, re.IGNORECASE)
    if full_date_match:
        month_name = full_date_match.group(1)
        day = full_date_match.group(2)
        year = full_date_match.group(3)
        
        month_map = {
            'jan': 1, 'feb': 2, 'mar': 3, 'apr': 4, 'may': 5, 'jun': 6,
            'jul': 7, 'aug': 8, 'sep': 9, 'oct': 10, 'nov': 11, 'dec': 12
        }
        
        month_num = month_map[month_name.lower()]
        return f"{year}-{month_num:02d}-{int(day):02d}"
    
    # If no pattern matches, return None or raise an exception
    return None

def extract_contact_info(contact):
    name_el = contact.query_selector("h3.msg-conversation-listitem__participant-names span.truncate")
    date_el = contact.query_selector("time.msg-conversation-listitem__time-stamp")

    if not name_el or not date_el:
        raise ValueError("Contact info not found")
    
    name = name_el.inner_text().strip()
    date_messaged = parse_date_str(date_el.inner_text().strip())

    return name, date_messaged

def extract_profile_url(page):
    page.wait_for_selector("div.msg-thread", timeout=10000)
    thread = page.query_selector("div.msg-thread")
    if not thread:
        raise ValueError("Message thread not found")

    link_el = thread.query_selector("a.msg-thread__link-to-profile")
    if not link_el:
        raise ValueError("LinkedIn URL not found")

    return link_el.get_attribute("href")

def extract_current_company(user_page):
    user_page.wait_for_selector("button[aria-label^='Current company']", timeout=5000)
    company_btn = user_page.query_selector("button[aria-label^='Current company']")
    company_string = company_btn.get_attribute("aria-label") if company_btn else ""
    match = re.search(r'Current company:\s*(.*?)\.', company_string)
    return match.group(1).strip() if match else "N/A"

def mark_unread(page, contact, date_messaged, name):
    page.wait_for_selector("div[id*='message-list-ember']", timeout=5000)
    messages = page.query_selector("div[id*='message-list-ember']")
    message_list = messages.query_selector_all("span[class*='msg-s-message-group__profile-link msg-s-message-group__name']")

    if message_list[-1].inner_text().strip() != name:
        # You were not the last person to message this person, so you can't mark it as unread
        return
    
    contact_date_updated = db.get_contact_date_updated(name)
    if contact_date_updated is None or contact_date_updated < date_messaged:
        if contact_date_updated is None:
            db.add_contact(name, date_messaged)
        else:
            db.update_contact_date_updated(name, date_messaged)

        try:
            # Click the "More options" (ellipsis) menu
            more_button = contact.query_selector('button:has(span:has-text("Open the options"))')
            if more_button:
                more_button.click()

                # Wait for the dropdown and click "Mark as unread"
                unread_option = contact.wait_for_selector('div[role="button"]:has-text("Mark as unread")')
                if contact.query_selector('div[role="button"]:has-text("Mark as unread")'):
                    unread_option.click()
                    print(f"Marked {name} as unread again")
        except Exception as e:
            print(f"Could not mark {name} as unread: {e}")

def get_recent_contacts():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64)...",
            viewport={"width": 1280, "height": 800}
        )

        page = context.new_page()
        page.goto("https://www.linkedin.com/messaging/")

        if "login" in page.url:
            login(page)
            page.goto("https://www.linkedin.com/messaging/")
        else:
            print("Already logged in")

        print("Scraping recent contacts...")
        captcha_frame = page.query_selector("iframe[src*='recaptcha']")
        if captcha_frame:
            print("Google reCAPTCHA detected")

        page.wait_for_selector("li[id*='ember'].msg-conversation-listitem", timeout=10000)
        contact_elements = page.query_selector_all("li[id*='ember'].msg-conversation-listitem")

        scraped_contacts = []
        for contact in contact_elements[:7]:  # Limit to 7 contacts
            try:
                # unread = True if contact.query_selector(".msg-conversation-card__unread-count .notification-badge__count") else False
                
                name, date_messaged = extract_contact_info(contact)
                print(f"Opening conversation with {name} on {date_messaged}")

                clickable = contact.query_selector("div.msg-conversation-listitem__link")
                if not clickable:
                    print(f"No clickable link for {name}")
                    continue
                clickable.click()

                linkedin_url = extract_profile_url(page)

                mark_unread(page, contact, date_messaged,name) # Marks unread if it was unread

                with context.new_page() as user_page:
                    user_page.goto(linkedin_url)
                    user_page.wait_for_load_state("load")

                    company = extract_current_company(user_page)

                scraped_contacts.append({
                    "Name": name,
                    "Company": company,
                    "LinkedIn URL": linkedin_url,
                    "Date Messaged": date_messaged
                })

            except Exception as e:
                print(f"Failed to process contact: {e}")
                continue
            finally:
                print("")

        print(f"Scraped {len(scraped_contacts)} contacts.")
        browser.close()
        return scraped_contacts