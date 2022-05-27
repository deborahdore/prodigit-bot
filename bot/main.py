import re
import threading

import telebot

from bot.login_dir.login_functions import call_booking_request, insert_matricola, user_exist, insert_password, \
    save_credentials
from bot.book_functions import booking_new_lesson, recap, booking_request, save_lesson
from bot.markup import start_markup, confirm_save_lesson_markup
from bot.utility import load_user_database, save_to_user_database, load_lessons_database

mutex = threading.Semaphore()
lessons = load_lessons_database(mutex)
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
- waiting for confirm
- waiting for book
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
    call_booking_request(call, mutex, bot, phases,lessons)


@bot.callback_query_handler(func=lambda call: call.data == "/reminder")
def handle_message(call):
    phases[call.message.chat.id] = "reminder"
    pass


@bot.callback_query_handler(func=lambda call: re.match("^/l", call.data))
def handle_message(call):
    phases[call.message.chat.id] = "waiting for confirm"
    recap(call, bot, phases, lessons)


@bot.callback_query_handler(func=lambda call: re.match("^/n_l", call.data))
def handle_message(call):
    phases[call.message.chat.id] = "waiting for confirm"
    recap(call, bot, phases, lessons)


@bot.callback_query_handler(func=lambda call: re.match("^/bk_", call.data))
def handle_message(call):
    phases[call.message.chat.id] = "start"
    if "/bk_no" == call.data:
        bot.send_message(call.message.chat.id,
                         "Okay! What  would you like to do:\n"
                         "1. Book a lecture \n"
                         "2. Manage reminders", reply_markup=start_markup())
    elif re.match("^/bk_n_", call.data):
        bot.send_message(call.message.chat.id, "Okay, I'm going to book it! Please Wait")
        saving_list = ""
        lesson_list = call.data.split("_")
        for i in range(2, len(lesson_list)):
            booking_request(lesson_list[i], mutex, bot, lessons)
            saving_list = saving_list + "_" + lesson_list[i]
        bot.send_message(call.message.chat.id,
                         "Done! Would you like to save this reservations infos for future reservation?\n"
                         , reply_markup=confirm_save_lesson_markup(saving_list))

    elif re.match("/bk_", call.data):
        bot.send_message(call.message.chat.id, "Okay, I'm going to book it! Please Wait")
        for lesson in call.data.split("_")[1:]:
            booking_request(lesson, mutex, bot, lessons)
        bot.send_message(call.message.chat.id, "All Done! What  would you like to do:\n"
                                               "1. Book a lecture \n"
                                               "2. Manage reminders", reply_markup=start_markup())


@bot.callback_query_handler(func=lambda call: re.match("^/s_", call.data))
def handle_message(call):
    phases[call.message.chat.id] = "waiting for confirm"

    if re.match("/s_no", call.data):
        pass
    elif re.match("^/s_", call.data):
        save_lesson(call, mutex, lessons)
    bot.send_message(call.message.chat.id, "All Done! What  would you like to do:\n"
                                           "1. Book a lecture \n"
                                           "2. Manage reminders", reply_markup=start_markup())


@bot.message_handler()
def main(message):
    phase = phases[message.chat.id]
    if phase == "book":
        booking_request(message, mutex, bot, phases)
    elif phase == "reminder":
        pass
    elif phase == "waiting for matricola":
        insert_matricola(message, mutex, bot, phases)
    elif phase == "waiting for password":
        insert_password(message, mutex, bot, phases)
    elif phase == "waiting for save credentials":
        save_credentials(message, mutex, bot, phases, lessons)
    if phase == "waiting for lesson name":
        booking_new_lesson(message, bot, phases, lessons)
    if phase == "waiting for confirm":
        pass


if __name__ == '__main__':
    bot.infinity_polling(interval=0, timeout=60)
