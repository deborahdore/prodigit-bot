import threading

import telebot

from bot.login_dir.login_functions import call_booking_request, insert_matricola, user_exist, insert_password, save_credentials
from bot.book_functions import booking_fork, booking_request
from bot.markup import start_markup
from bot.utility import load_user_database, save_to_user_database

mutex = threading.Semaphore()

bot = telebot.TeleBot("5214072158:AAGj-lZig1CmTn06nI7JBiTH7nbm1grlv_I")
phases = {}

'''
- start
- book
- reminder
- waiting for matricola
- waiting for password
- waiting for save credentials
- waiting for lesson name
'''


@bot.message_handler(commands=['start'])
def handle_start_help(message):
    # salva utente allo start se non già presente
    if not user_exist(message.from_user.id, mutex):
        database = load_user_database(mutex)
        database[message.from_user.id] = {
            "matricola": "",
            "password": "",
            "token": "",
            "login": False,
            "saved_lessons": [],
            "weekly_reminders": False,
            "daily_reminders": False
        }
        save_to_user_database(database, mutex)

    phases[message.chat.id] = "start"

    bot.send_message(message.chat.id,
                     "Hello! I'm a Bot made to make the life of Sapienza' student easy. Here's a list of what you can do:\n"
                     "1. Book a lecture \n"
                     "2. Manage reminders", reply_markup=start_markup())


@bot.callback_query_handler(func=lambda call: call.data == "/book")
def handle_message(call):
    phases[call.message.chat.id] = "book"
    call_booking_request(call, mutex, bot, phases)


@bot.callback_query_handler(func=lambda call: call.data == "/reminder")
def handle_message(call):
    phases[call.message.chat.id] = "reminder"
    pass

@bot.callback_query_handler(func=lambda call: call.data == "/lesson*")
def handle_message(call):
    phases[call.message.chat.id] = "start"
    call_booking_request(call, mutex, bot, phases)

@bot.callback_query_handler(func=lambda call: call.data == "/new_lesson*")
def handle_message(call):
    phases[call.message.chat.id] = "start"
    call_booking_request(call, mutex, bot, phases)
    bot.send_message("fatto!")

@bot.message_handler()
def main(message):
    phase = phases[str(message.chat.id)]
    if phase == "book":
        booking_request(message, mutex, bot, phases)
    elif phase == "reminder":
        pass
    elif phase == "waiting for matricola":
        insert_matricola(message, mutex, bot, phases)
    elif phase == "waiting for password":
        insert_password(message, mutex, bot, phases)
    elif phase == "waiting for save credentials":
        save_credentials(message, mutex, bot, phases)
    if phase == "waiting for lesson name":
        booking_fork(message,mutex,bot,phases)



if __name__ == '__main__':
    bot.infinity_polling(interval=0, timeout=60)
