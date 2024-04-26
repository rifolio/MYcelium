import requests
import time
import sqlite3
from email_actions import EmailActions


class HubSpotNewContacts:
    def __init__(self, access_token):
        self.access_token = access_token
        self.endpoint = 'https://api.hubapi.com/crm/v3/objects/contacts'
        self.existing_contact_ids = set()

        #Connect to SQLite database
        self.conn = sqlite3.connect('newContacts.db')
        self.create_table()

    def create_table(self):
        #Create contacts table if not exists
        cursor = self.conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS contacts (
                            id INTEGER PRIMARY KEY,
                            firstname TEXT,
                            lastname TEXT,
                            email TEXT,
                            phone TEXT
                          )''')
        self.conn.commit()

    def insert_contact(self, contact):
        cursor = self.conn.cursor()
        cursor.execute('''INSERT INTO contacts (id, firstname, lastname, email, phone)
                          VALUES (?, ?, ?, ?, ?)''',
                       (contact['id'],
                        contact['properties'].get('firstname', 'N/A'),
                        contact['properties'].get('lastname', 'N/A'),
                        contact['properties'].get('email', 'N/A'),
                        contact['properties'].get('phone', 'N/A')))
        self.conn.commit()

    def get_contacts(self): #from our code
        headers = {'Authorization': f'Bearer {self.access_token}'}
        params = {'properties': 'id,firstname,lastname,email,phone'}
        response = requests.get(self.endpoint, headers=headers, params=params)
        if response.status_code == 200:
            return response.json().get('results', [])
        else:
            print(f"Failed to retrieve contacts: {response.status_code}")
            return []

    def check_for_new_contacts(self):
        new_contacts = self.get_contacts()
        for contact in new_contacts:
            contact_id = contact['id']
            if contact_id not in self.existing_contact_ids:
                self.existing_contact_ids.add(contact_id)
                print("New contact added")
                self.insert_contact(contact)

    def run(self, email_actions:EmailActions): #loop and only keep existing contacts based on ID
        existing_contacts = self.get_contacts()
        for contact in existing_contacts:
            self.existing_contact_ids.add(contact['id'])
        while True:
            self.check_for_new_contacts()
            time.sleep(10) #in seconds
            email_actions.send_emails_and_clear_database()

    def __del__(self):
        #Close database connection when object is deleted
        self.conn.close()