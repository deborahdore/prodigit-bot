import re
import threading
from datetime import datetime, time

import schedule
import telebot

from bot.book_dir.book import booking_request
from bot.book_dir.book_functions import booking_new_lesson, recap, save_lesson, message_booking_request
from bot.login_dir.login_functions import call_booking_request, insert_matricola, user_exist, insert_password, \
    save_credentials
from bot.markup import confirm_save_lesson_markup
from bot.markup import start_markup, reminder_markup
from bot.reminder_functions import manage_reminder
from bot.utility import load_lessons_database
from bot.utility import load_user_database, save_to_user_database

mutex = threading.Semaphore()
lessons = load_lessons_database()
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


@bot.message_handler(commands=['book'])
def handle_start_help(message):
    message_booking_request(message, mutex, bot, phases, lessons)


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
            "daily_reminders": False,
            "chat_id": message.chat.id,
            "timestamp_token": str(datetime.today().strftime('%Y-%m-%d %H:%M:%S'))
        }
        save_to_user_database(database, mutex)

    phases[message.chat.id] = "start"

    bot.send_message(message.chat.id,
                     "Hello! I'm a Bot made to make the life of Sapienza' student easy. Here's a list of what you can do:\n"
                     "1. Book a lecture \n"
                     "2. Manage reminders", reply_markup=start_markup())


@bot.callback_query_handler(func=lambda call: re.match("^save_credentials", call.data))
def handle_message(call):
    phases[call.message.chat.id] = "waiting for lesson name"
    save_credentials(call.data, str(call.from_user.id), call.message.chat.id, mutex, bot, phases, lessons)


@bot.callback_query_handler(func=lambda call: call.data == "/book")
def handle_message(call):
    phases[call.message.chat.id] = "book"
    call_booking_request(call.from_user.id, call.message.chat.id, mutex, bot, phases, lessons)


@bot.callback_query_handler(func=lambda call: call.data == "/reminders")
def handle_message(call):
    phases[call.message.chat.id] = "reminder"
    database = load_user_database(mutex)
    flag_w = database[str(call.from_user.id)]["weekly_reminders"]
    flag_d = database[str(call.from_user.id)]["daily_reminders"]
    bot.send_message(call.message.chat.id, "What do you want to do? \n\n"
                                           "The weekly reminder will warn you every Sunday at 5pm to book the lessons "
                                           "for the following week \n\nThe lesson reminder will warn you the day before "
                                           "each lesson to remind you cancel it, if you are not going to attend\n\n"
                                           "If you have already set a reminder you will have the option to disable it",
                     reply_markup=reminder_markup(flag_w, flag_d))


@bot.callback_query_handler(func=lambda call: re.match('^[rem]', call.data))
def callback_query(call):
    phase = phases[call.message.chat.id]
    if phase == "reminder":
        manage_reminder(call, mutex, bot, phases)


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
            # QUA C'è UN PROBLEMA: lesson_list[i] passa solo il primo numero
            booking_request(lesson_list[i], mutex, bot, lessons, call, phases)
            saving_list = saving_list + "_" + lesson_list[i]
        bot.send_message(call.message.chat.id,
                         "Done! Would you like to save this reservations infos for future reservation?\n"
                         , reply_markup=confirm_save_lesson_markup(saving_list))

    elif re.match("/bk_", call.data):
        bot.send_message(call.message.chat.id, "Okay, I'm going to book it! Please Wait")
        for lesson in call.data.split("_")[1:]:
            booking_request(lesson, mutex, bot, lessons, call, phases)
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
        message_booking_request(message, mutex, bot, phases, lessons)
    elif phase == "reminder":
        pass
    elif phase == "waiting for matricola":
        insert_matricola(message, mutex, bot, phases)
    elif phase == "waiting for password":
        insert_password(message, mutex, bot, phases)
    elif phase == "waiting for save credentials":
        save_credentials(message.text, str(message.from_user.id), message.chat.id, mutex, bot, phases, lessons)
    if phase == "waiting for lesson name":
        booking_new_lesson(message, bot, phases, lessons)
    if phase == "waiting for confirm":
        pass


schedule.every(10).minutes.do(funzione())
schedule.every().hour.do(funzione())
schedule.every().day.at("10:30").do(funzione())
schedule.every().monday.do(funzione())
schedule.every().wednesday.at("13:15").do(funzione())
schedule.every().minute.at(":17").do(funzione())


def thread_function():
    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == '__main__':
    x = threading.Thread(target=thread_function, args=("ciao",), daemon=True)
    x.start()
    bot.infinity_polling(interval=0, timeout=60)
