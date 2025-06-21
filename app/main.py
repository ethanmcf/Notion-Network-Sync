from handlers.linkedin_handler import get_recent_contacts
from handlers.notion_handler import add_contacts_to_notion
from handlers.gpt_handler import generate_response

def main():
    # contacts = get_recent_contacts()
    # contacts = [{'Name': 'Danielle Sacks', 'Company': 'John Howard Society of Ontario', 'LinkedIn URL': 'https://www.linkedin.com/in/ACoAAEgFDWsBsrH0ofD2JcQYI7G1mCEZadSSK6g', 'Date Messaged': '2025-06-20'}, {'Name': 'Osama Saleh', 'Company': 'LinkedIn', 'LinkedIn URL': 'https://www.linkedin.com/in/ACoAABzhoBABqIgmHo2YYmPyxwgxtb8NCgTo5sc', 'Date Messaged': '2025-06-20'}]
    # add_contacts_to_notion(contacts)
    generate_response("""Amazon - micro managed environment

Loadtest tool that they maintained run some systhenetic tests against database - internship project

Explore more - ask more questions how do they organize their day, agree

Maintain graph database - any query that goes through linkedin ie for followers, connection

Economic graph - representation of global economey (people conected with skills, etc)
2 aspects - legacy system and builing new database 

He works on query engine optimization - then translates it to relational algebra, storage, injestion how data is inserted into the database 

He worked infra in internships, 

CSC367 - parallel programming

CSC443 - database systems (great prof) pieces together stuff from 369 to real world application 

CSC324 - principles 

compliers course 

CSC469 - 

Wiling to send resume

Side projects - algo visualizer (ie bfs, etc) & job portal for research applications

Didn’t really have referrals - strong referal at Meta, Tesla

Ping recuiters multiple times, every day

Practice speaking 

Mock interviews - [interviewing.io](http://interviewing.io) - great [pramp.com](http://pramp.com) - too easy""")

if __name__ == "__main__":
    main() 