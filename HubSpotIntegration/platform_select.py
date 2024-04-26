from email_actions import EmailActions
from Hubspot_New_Contacts import HubSpotNewContacts
import os

# Load environment variables from .env file
from dotenv import load_dotenv
load_dotenv()


#This class runs all the interactions. Prob should go inside the main
class PlatformSelect:
    def __init__(self):
        pass

    def select_platform(self):
        platform = input("Pick a platform (1. Hubspot, 2. N/A): ")
        if platform == "1":
            return self.select_event()
        elif platform == "2":
            print("Coming soon")
        else:
            print("Invalid choice")
            return None

    def select_event(self):
        event = input("Select an event from Hubspot (1. New contact, 2. New deal, 3. N/A): ")
        if event == "1":
            return "HubspotNewContacts"
        elif event == "2":
            print("New deal functionality not implemented yet")
            return None
        elif event == "3":
            print("Coming soon")
            return None
        else:
            print("Invalid choice")
            return None

    def contacts_actions(self):
        action = input("What action would you like? (1. Email, 2. Sort by Newest, 3. N/A): ")
        if action == "1":
            return "send_email"
        elif action == "2":
            print("Coming soon")
            return None
        elif action == "3":
            print("Coming soon")
            return None
        else:
            print("Invalid choice")
            return None

    def send_email(self):
        event = input("What would you like to email? (1. Send an Email, 2. N/A): ")
        if event == "1":
            return "send_email_to_new_contacts"
        elif event == "2":
            print("Coming soon")
            return None
        else:
            print("Invalid choice")
            return None

#start the class
platform_select = PlatformSelect()

#Collect user inputs
#This was written like this as in the start the classes were called under wheere the choices for them were made. This caused an issue with the hubspot class where it wouldnt let the code contiue as it has a while loop inside
platform_selection = platform_select.select_platform()
if platform_selection == "HubspotNewContacts":
    contacts_action = platform_select.contacts_actions()
    if contacts_action == "send_email":
        email_action = platform_select.send_email()
        if email_action == "send_email_to_new_contacts":
            # Instantiate and run the HubSpotNewContacts class
            access_token_hubspot = os.getenv('HUBSPOT_ACCESS_TOKEN')  #token
            hubspot_manager = HubSpotNewContacts(access_token_hubspot) #friend helped me fix my loops
            Email=EmailActions()
            hubspot_manager.run(Email)