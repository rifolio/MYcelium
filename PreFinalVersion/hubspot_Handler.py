import requests

"""
This class interacts with the HubSpot API to retrieve contacts and send data to HubSpot.
"""


class HubspotHandler:
    def __init__(self, access_token_hubspot):
        self.access_token_hubspot = access_token_hubspot
        self.endpoint = 'https://api.hubapi.com/crm/v3/objects/contacts'

    def get_contacts(self):
        headers = {'Authorization': f'Bearer {self.access_token_hubspot}'}
        params = {'properties': 'id,firstname,lastname,email,phone'}
        response = requests.get(self.endpoint, headers=headers, params=params)
        if response.status_code == 200:
            return response.json().get('results', [])
        else:
            print(f"Failed to retrieve contacts: {response.status_code}")
            return []

    def upload_contacts(self, contacts):
        url = "https://api.hubapi.com/crm/v3/objects/contacts"
        headers = {"Authorization": f"Bearer {self.access_token_hubspot}", "Content-Type": "application/json"}

        for contact in contacts:
            payload = {
                "properties": {
                    "firstname": contact[1],  # First Name
                    "lastname": contact[2],  # Last Name
                    "email": contact[0],  # Email
                    "phone": contact[3],  # Phone Number
                }
            }

            try:
                response = requests.post(url, headers=headers, json=payload)
                response.raise_for_status()
                print("Contact added successfully.")
            except requests.exceptions.RequestException as e:
                print("Failed to add contact:", e)
