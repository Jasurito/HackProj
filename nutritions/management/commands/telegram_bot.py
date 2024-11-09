import os
import django
import telebot
import schedule
import time
import threading
import datetime
from django.core.management.base import BaseCommand
from django.contrib.auth import authenticate


# Set up Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'HackProj.settings')
django.setup()

from nutritions.models import User, UserInfo, UserSchedule

API_KEY = '7830840669:AAF69IRMrusjVQuKssAjAmQCnPUD1seG1g0'
bot = telebot.TeleBot(API_KEY, parse_mode=None)

# Dictionary to temporarily store logged-in users' data
logged_in_users = {}

def User_Object(username):
    user = User.objects.get(username=username)
    user1 = UserInfo.objects.get(user=user)
    user2 = UserSchedule.objects.get(user_info=user1)
    return user2


def send_meal_message(chat_id, message_text):
    bot.send_message(chat_id, message_text)

def send_breakfast():
    for chat_id in logged_in_users.keys():
        user_info = logged_in_users[chat_id]
        try:
            schedule = UserSchedule.objects.get(user_info=user_info)
            message = f"Good morning! Here’s your breakfast:\n{schedule.monday_break}"
            send_meal_message(chat_id, message)
        except UserSchedule.DoesNotExist:
            pass

def send_lunch():
    for chat_id in logged_in_users.keys():
        user_info = logged_in_users[chat_id]
        try:
            schedule = UserSchedule.objects.get(user_info=user_info)
            message = f"Lunchtime! Here’s your lunch:\n{schedule.monday_lunch}"
            send_meal_message(chat_id, message)
        except UserSchedule.DoesNotExist:
            pass

def send_dinner():
    for chat_id in logged_in_users.keys():
        user_info = logged_in_users[chat_id]
        try:
            schedule = UserSchedule.objects.get(user_info=user_info)
            message = f"Dinner time! Here’s your dinner:\n{schedule.monday_dinner}"
            send_meal_message(chat_id, message)
        except UserSchedule.DoesNotExist:
            pass

# Bot Command to Start the Bot
@bot.message_handler(commands=['start'])
def start(msg):
    bot.reply_to(msg, "Hello! Type /login to log in to your account.")

# Bot Command to Begin Login Process
@bot.message_handler(commands=['login'])
def login(msg):
    chat_id = msg.chat.id
    bot.reply_to(msg, "Enter Your Username:")
    bot.register_next_step_handler(msg, process_username)

def process_username(msg):
    chat_id = msg.chat.id
    username = msg.text
    logged_in_users[chat_id] = {'username':username}  # Temporarily store username
    bot.reply_to(msg, "Enter Your Password:")
    bot.register_next_step_handler(msg, process_password)

def process_password(msg):
    chat_id = msg.chat.id
    password = msg.text
    username = logged_in_users[chat_id].get('username')
    # Authenticate user
    user = authenticate(username=username, password=password)
    if user is not None:
        try:
            user_info = UserInfo.objects.get(user=user)
            user_info.telegram_id = msg.chat.id
            user_info.save()
            logged_in_users[chat_id] = user_info  # Store UserInfo instance after successful login
            bot.reply_to(msg, "Login successful! You will now receive meal reminders.")
        except UserInfo.DoesNotExist:
            bot.reply_to(msg, "User information not found.")
    else:
        bot.reply_to(msg, "Invalid username or password.")
        logged_in_users.pop(chat_id, None)  # Remove entry if login failed

# Function to run the schedule in a separate thread
def run_schedule():
    while True:
        schedule.run_pending()
        time.sleep(60)

# Define the Command Class
class Command(BaseCommand):
    help = "Runs the Telegram bot to send meal notifications"

    def handle(self, *args, **kwargs):
        # Schedule the tasks
        schedule.every().day.at("08:00").do(send_breakfast)
        schedule.every().day.at("12:00").do(send_lunch)
        schedule.every().day.at("18:00").do(send_dinner)

        # Start the schedule in a new thread
        schedule_thread = threading.Thread(target=run_schedule)
        schedule_thread.start()

        # Start polling
        print("Bot started and schedule initialized.")
        bot.polling()