import os
import pandas as pd
from dotenv import load_dotenv
from regex import DataAnalyzer, DataSpliter
from hubspot_Handler import HubspotHandler
from reader_Adapter import CSVReader, ExcelReader
from sql_Handler import SQLHandler
from telebot import TeleBot, types

class Main():
    def __init__(self):
        #Load environment variables from .env file
        load_dotenv()
        self.access_token_hubspot = os.getenv("HUBSPOT_ACCESS_TOKEN")
        self.sql_handler = SQLHandler('MyCelium Database.db')
        self.sql_handler.drop_all_tables()  #Drop all tables when initializing MyCelium

        #Initialize Telegram bot
        self.bot = TeleBot(os.getenv("TELEGRAM_TOKEN"))

        #Setup Telegram bot handlers
        self.setup_handlers()

    def setup_handlers(self):
        @self.bot.message_handler(commands=['start'])
        def start(message):
            self.start(message)

        @self.bot.message_handler(content_types=["text"], func=lambda message: message.text == "Update")
        def update_data(message):
            self.update_data(message)

        @self.bot.message_handler(func=lambda message: message.text == "AI")
        def handle_ai(message):
            self.handle_ai(message)

    def start(self, message):
        #Keyboard markup for options
        markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
        migrate_button = types.KeyboardButton('Migrate')
        update_button = types.KeyboardButton('Update')
        markup.row(migrate_button, update_button)

        #Welcome message and riddle
        welcome_message = ("Welcome to MyCelium 5.63!\n\n"
                          "Try to solve this riddle till we heat things up!\n"
                          "I am the mind without a brain, Yet I can think. "
                          "Invisible hands, my workings unseen, I am everywhere, yet never been. What am I?\n\n"
                          "Answer: I am AI!\n\n"
                          "Let's get started")

        self.bot.send_message(message.chat.id, welcome_message)
    
    def update_data(self, message):
        #Ask user for file name or Path in our case
        self.bot.send_message(message.chat.id, "Please enter the file path:")
        
        @self.bot.message_handler(func=lambda message: True)
        def get_file_name(message):
            if message.text:
                input_file = message.text.strip('"')

                analyze = DataAnalyzer(input_file)
                regex_data = DataSpliter()

                labeled, leftover = regex_data.split_and_save(analyze)

                formated_data = pd.merge(labeled, leftover, how='outer', left_index=True, right_index=True)
                #Save the DataFrame to a CSV file
                formated_data.to_csv('Data/output_file.csv', index=False)

                input_file = 'Data/output_file.csv'

                #Create SQL database
                table_name = os.path.splitext(os.path.basename(input_file))[0]  #Extract table name from file name
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
                    print("Contacts from the database:", contacts)  #Debug print

                    destination = input("Where do you want to send the data? (H for HubSpot) (More to come...): ")
                    if destination.upper() == 'H':
                        print("The dataset is a Contacts dataset!")
                        hubspot_handler = HubspotHandler(self.access_token_hubspot)  #Create instance of HubspotHandler

                        #Retrieve contacts from HubSpot and save them to the database
                        hubspot_contacts = hubspot_handler.get_contacts()
                        self.sql_handler.write_contacts_from_hubspot(hubspot_contacts, table_name)
                        print("Contacts from HubSpot saved to the database.")

                        #Call upload_contacts method
                        hubspot_handler.upload_contacts(contacts)
                        print("Contacts uploaded to HubSpot.")

                    else:
                        print("Invalid destination choice. Please choose 'H' for HubSpot.")

                    #Print confirmation message and send keyboard again
                    self.bot.send_message(message.chat.id, "Thank you!")
                    self.start(message)

                except FileNotFoundError:
                    print("File not found. Please make sure you've entered the correct file path.")
                except Exception as e:
                    print(f"An error occurred: {e}")
            else:
                #If no input is provided, prompt again
                self.bot.send_message(message.chat.id, "Please enter a valid file name:")

    def run(self):
        self.bot.polling()

if __name__ == "__main__":
    app = Main()
    print('Started pooling...')
    app.run()