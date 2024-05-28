import requests

"""
This class interacts with the HubSpot API to retrieve contacts and send data to HubSpot.
"""


class HubspotHandler:
    def __init__(self, access_token_hubspot):
        #Initialize Hubspot API with token
        self.access_token_hubspot = access_token_hubspot
        #endpoint for contacts
        self.endpoint = 'https://api.hubapi.com/crm/v3/objects/contacts'

    def get_contacts(self):
        #Setup headers with authorization token
        headers = {'Authorization': f'Bearer {self.access_token_hubspot}'}

        #pPrameters to reequest chosen contacts properties rather than all
        params = {'properties': 'id,firstname,lastname,email,phone'}
        #A GET requestto HubSpot
        response = requests.get(self.endpoint, headers=headers, params=params)
        if response.status_code == 200:
            return response.json().get('results', [])
        else:
            print(f"Failed to retrieve contacts: {response.status_code}")
            return []

    def upload_contacts(self, contacts):
        #Endpoint for uploading contacts
        url = "https://api.hubapi.com/crm/v3/objects/contacts"
        headers = {"Authorization": f"Bearer {self.access_token_hubspot}", "Content-Type": "application/json"}
        #Loop through each contact and upload it
        for contact in contacts:
            payload = {
                "properties": {
                    "firstname": contact[2],  #First Name
                    "lastname": contact[3],  #Last Name
                    "email": contact[1],  #Email
                    "phone": contact[0],  #Phone Number
                }
            }

            try:
                #Make a POST request to add the contacts
                response = requests.post(url, headers=headers, json=payload)
                response.raise_for_status()
                print("Contact added successfully.")
            except requests.exceptions.RequestException as e:
                print("Failed to add contact:", e)

