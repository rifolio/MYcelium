# Created by:

# Vladyslav Horbatenko - https://github.com/rifolio
# Salar Komeyshi - https://github.com/SalarKo
# Kacper Hvid - https://github.com/KacperPuzniak

import os
import pandas as pd
from dotenv import load_dotenv
from regex import DataAnalyzer, DataTypeChecker, DataSpliter, TypeChecker
from hubspot_Handler import HubspotHandler
from reader_Adapter import CSVReader, ExcelReader
from sql_Handler import SQLHandler
from ai import AIModel


class Main():
    def __init__(self):
        #Load environment variables from .env file
        load_dotenv()
        self.access_token_hubspot = os.getenv("HUBSPOT_ACCESS_TOKEN")
        self.sql_handler = SQLHandler('MyCelium Database.db')
        self.sql_handler.drop_all_tables()  #Drop all tables when initializing MyCelium

        print("Welcome to MyCelium 5.63!")
        print("\nTry to solve this riddle till we heat things up!")
        print("I am the mind without a brain, Yet I can think. Invisible hands, my workings unseen, I am everywhere, yet never been. What am I?")

        # Load AI model and train it
        self.ai_model = AIModel()
        self.ai_model.train_ai()

        print("Answer: I am AI!")
        print("\nLet's get started")

    def myCelium(self):
        entry = input("Would you like to Upload (U) or Migrate (M) your data? ").strip().upper()

        if entry == "M":
            print("PLACEHOLDER FOR MIGRATION")  # MIGRATION # Future stuff

        if entry == "U":
            input_file = input("Please enter the file name: ").strip('"')

            analyze = DataAnalyzer(input_file)
            regex_data = DataSpliter()

            labeled, leftover = regex_data.split_and_save(analyze)

            formated_data = pd.merge(labeled, leftover, how='outer', left_index=True, right_index=True)
            #Save the DataFrame to a CSV file
            input_file = formated_data.to_csv('output_file.csv', index=False)

            #Create SQL database
            table_name = os.path.splitext(os.path.basename(input_file))[0]  # Extract table name from file name
            try:
                self.sql_handler.create_table(input_file)
                source_data = []

                #Determine the file type (CSV or Excel) based on the file extension
                file_extension = os.path.splitext(input_file)[1]
                if file_extension.lower() == '.csv':
                    source_data = CSVReader.read_csv(input_file)
                elif file_extension.lower() in ['.xls', '.xlsx']:
                    source_data = ExcelReader.read_excel(input_file)
                else:
                    print("Unsupported file type. Please provide a CSV or Excel file.")

                #Ensure data is available before proceeding
                if not source_data:
                    print("No data found in the file.")
                    return

                #Use SQLHandler to write data to the database
                self.sql_handler.write_data(source_data, table_name)

                #Read contacts from the database
                contacts = self.sql_handler.read_contacts(table_name)
                print("Contacts from the database:", contacts)  # Debug print

                destination = input("Where do you want to send the data? (H for HubSpot) (More to come...): ")
                if destination.upper() == 'H':
                    #AI prediction
                    prediction = self.ai_model.predict_result(input_file)

                    if prediction == 'Contacts':
                        print("The dataset is a Contacts dataset!")
                        hubspot_handler = HubspotHandler(self.access_token_hubspot)  # Create instance of HubspotHandler

                        #Retrieve contacts from HubSpot and save them to the database
                        hubspot_contacts = hubspot_handler.get_contacts()
                        self.sql_handler.write_contacts_from_hubspot(hubspot_contacts, table_name)
                        print("Contacts from HubSpot saved to the database.")

                        #Call upload_contacts method
                        hubspot_handler.upload_contacts(contacts)
                        print("Contacts uploaded to HubSpot.")

                    else:
                        print("Products")
                        #Call upload_contacts method
                        #hubspot_handler.upload_products(products)
                        print("Contacts uploaded to HubSpot.")

                else:
                    print("Invalid destination choice. Please choose 'H' for HubSpot.")

            except FileNotFoundError:
                print("File not found. Please make sure you've entered the correct file path.")
            except Exception as e:
                print(f"An error occurred: {e}")


if __name__ == "__main__":
    app = Main()
    app.myCelium()
