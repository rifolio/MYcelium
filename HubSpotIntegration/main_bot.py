import telebot
from telebot import types
from email_actions import EmailActions
from Hubspot_New_Contacts import HubSpotNewContacts
import config
import os

# Load environment variables from .env file
from dotenv import load_dotenv
load_dotenv()

class MyCeliumBot:
    def __init__(self):
        self.bot = telebot.TeleBot(config.TOKEN)
        self.setup_handlers()

    def start(self, message):
        keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
        markup = types.ReplyKeyboardMarkup()
        text = "Hello {0.first_name} 👋\nWelcome to MyCelium Bot. Here you can access and manage data from different CRMs.".format(
            message.from_user)
        hubspot = types.KeyboardButton('HubSpot')
        other_crm = types.KeyboardButton('Other')
        keyboard.add(hubspot, other_crm)
        markup.row(hubspot, other_crm)
        self.bot.send_message(message.chat.id, text, reply_markup=keyboard)

    def hubspot_comp(self, message):
        markup = types.ReplyKeyboardMarkup(row_width=4, resize_keyboard=True)
        new_contact = types.KeyboardButton('New Contact')
        new_deal = types.KeyboardButton('New Deal')
        other_event = types.KeyboardButton('Other')
        back = types.KeyboardButton('Go back ◀️')
        markup.add(new_contact, new_deal, other_event, back)
        self.bot.send_message(message.chat.id, 'Select an event from HubSpot', reply_markup=markup)

    def new_contact(self, message):
        markup = types.ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)
        email_action = types.KeyboardButton('Email')
        sort_action = types.KeyboardButton("Sort by Newest")
        other_action = types.KeyboardButton("Other")
        markup.add(email_action, sort_action, other_action)
        self.bot.send_message(message.chat.id, "What Action would you like?", reply_markup=markup)

    def action_email(self, message):
        markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
        email_handle = types.KeyboardButton("Send an email")
        other_handle = types.KeyboardButton("Other")
        markup.add(email_handle, other_handle)
        self.bot.send_message(message.chat.id, "What would you like to email?", reply_markup=markup)

    def send_email(self, message):
        markup = types.ReplyKeyboardMarkup(row_width=4, resize_keyboard=True)
        back = types.KeyboardButton('Go Back ◀️')
        markup.add(back)
        self.bot.send_message(message.chat.id, "NOW WE CALL FUNCTION FROM HUBSPOT OOP CODE", reply_markup=markup)
        access_token_hubspot = os.getenv('HUBSPOT_ACCESS_TOKEN')  # token
        hubspot_manager = HubSpotNewContacts(access_token_hubspot)
        email = EmailActions()
        hubspot_manager.run(email)

    def setup_handlers(self):
        @self.bot.message_handler(commands=['start'])
        def start(message):
            self.start(message)

        @self.bot.message_handler(content_types=["text"], func=lambda message: message.text == "HubSpot")
        def hubspot_comp(message):
            self.hubspot_comp(message)

        @self.bot.message_handler(content_types=["text"], func=lambda message: message.text == "New Contact")
        def new_contact(message):
            self.new_contact(message)

        @self.bot.message_handler(content_types=["text"], func=lambda message: message.text == "Email")
        def action_email(message):
            self.action_email(message)

        @self.bot.message_handler(content_types=["text"], func=lambda message: message.text == "Send an email")
        def back(message):
            self.send_email(message)

    def run(self):
        self.bot.polling()

if __name__ == "__main__":
    bot = MyCeliumBot()
    bot.run()
