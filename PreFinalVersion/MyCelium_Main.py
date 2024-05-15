import os
from dotenv import load_dotenv
from hubspot_Handler import HubspotHandler
from reader_Adapter import CSVReader, ExcelReader
from sql_Handler import SQLHandler
from data_Formatter import DataFormatter

load_dotenv()


class MyCelium:
    def __init__(self):
        self.access_token_hubspot = os.getenv("HUBSPOT_ACCESS_TOKEN")
        self.sql_handler = SQLHandler('MyCelium Database.db')
        self.sql_handler.drop_all_tables()  # Drop all tables when initializing MyCelium

    def main(self):
        print("Welcome to MyCelium 2.0!")
        entry = input("Would you like to Upload(U) or Migrate (M) data? ").strip().upper()

        if entry == "M":
            print("PLACEHOLDER FOR MIGRATION")  ## MIGRATION

        elif entry == "U":
            input_file = input("Please enter the file name: ").strip('"')
            table_name = os.path.splitext(os.path.basename(input_file))[0]  # Extract table name from file name
            try:
                self.sql_handler.create_table(input_file)
                source_contacts = []

                # Determine the file type (CSV or Excel) based on the file extension
                file_extension = os.path.splitext(input_file)[1]
                if file_extension.lower() == '.csv':
                    source_contacts = CSVReader.read_csv(input_file)
                elif file_extension.lower() in ['.xls', '.xlsx']:
                    source_contacts = ExcelReader.read_excel(input_file)
                else:
                    print("Unsupported file type. Please provide a CSV or Excel file.")

                # Ensure data is available before proceeding
                if not source_contacts:
                    print("No contacts found in the file.")
                    return

                # Use SQLHandler to write contacts to the database
                self.sql_handler.write_contacts(source_contacts, table_name)

                # Read contacts from the database
                contacts = self.sql_handler.read_contacts(table_name)
                print("Contacts from the database:", contacts)  # Debug print

                destination = input("Where do you want to send the data? (H for HubSpot): ")
                if destination.upper() == 'H':
                    hubspot_handler = HubspotHandler(self.access_token_hubspot)  # Create instance of HubspotHandler

                    # Retrieve contacts from HubSpot and save them to the database
                    hubspot_contacts = hubspot_handler.get_contacts()
                    self.sql_handler.write_contacts_from_hubspot(hubspot_contacts, table_name)
                    print("Contacts from HubSpot saved to the database.")

                    # Schema matching using DataFormatter
                    destination_csv = "HubSpot"
                    formatted_data = DataFormatter.match_schema(input_file, destination_csv)
                    print("Formatted data after schema matching:")
                    print(formatted_data)

                    # Save formatted data as a new table in the database
                    formatted_table_name = f"{table_name}_formatted"
                    self.sql_handler.create_table_from_data(formatted_data, formatted_table_name)
                    print(f"Formatted data saved as table '{formatted_table_name}' in the database.")

                    # Call upload_contacts method
                    hubspot_handler.upload_contacts(contacts)
                    print("Contacts uploaded to HubSpot.")

                else:
                    print("Invalid destination choice. Please choose 'H' for HubSpot.")

            except FileNotFoundError:
                print("File not found. Please make sure you've entered the correct file path.")
            except Exception as e:
                print(f"An error occurred: {e}")


if __name__ == "__main__":
    app = MyCelium()
    app.main()