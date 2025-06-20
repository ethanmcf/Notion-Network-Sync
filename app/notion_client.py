# import os
# from notion_client import Client
# from dotenv import load_dotenv

# load_dotenv()

# NOTION_API_KEY = os.getenv("NOTION_API_KEY")
# DATABASE_ID = os.getenv("DATABASE_ID")

# notion = Client(auth=NOTION_API_KEY)

# def add_contacts_to_notion(contacts):
#     for contact in contacts:
#         try:
#             notion.pages.create(
#                 parent={"database_id": DATABASE_ID},
#                 properties={
#                     "Name": {"title": [{"text": {"content": contact["Name"]}}]},
#                     "Company": {"rich_text": [{"text": {"content": contact["Company"]}}]},
#                     "LinkedIn URL": {"url": contact["LinkedIn URL"]},
#                     "Message": {"rich_text": [{"text": {"content": contact["Message"]}}]},
#                     "Date Messaged": {"date": {"start": contact["Date Messaged"]}},
#                 },
#             )
#         except Exception as e:
#             print(f"Failed to add contact {contact['Name']}: {e}") 