import time

from bot.utility import save_to_user_database, load_user_database
from datetime import datetime


def manage_reminder(call, mutex, bot, phases):
    database = load_user_database(mutex)
    chat_id = call.message.chat.id
    flag_w = database[str(call.from_user.id)]["weekly_reminders"]
    flag_d = database[str(call.from_user.id)]["daily_reminders"]

    if call.data == "rem_sw":
        flag_w = True
        bot.send_message(chat_id, "Done! You will receive a reminder every Sunday at 5pm")
    elif call.data == "rem_sd":
        flag_d = True
        bot.send_message(chat_id, "Done! You will receive a reminder 24 hours before each lesson booked using the bot")
    elif call.data == "rem_sb":
        flag_w = True
        flag_d = True
        bot.send_message(chat_id, "Done! You will receive a reminder every Sunday at 5pm and "
                                  "24 hours before each lesson booked using the bot")
    elif call.data == "rem_dw":
        flag_w = False
        bot.send_message(chat_id, "Done! You won't receive a weekly message")
    elif call.data == "rem_dd":
        flag_d = False
        bot.send_message(chat_id, "Done! You won't receive a reminder before the lessons")
    elif call.data == "rem_db":
        flag_w = False
        flag_d = False
        bot.send_message(chat_id, "Done! You won't receive any reminder")

    database[str(call.from_user.id)]["weekly_reminders"] = flag_w
    database[str(call.from_user.id)]["daily_reminders"] = flag_d
    save_to_user_database(database, mutex)

def send_weekly_reminders(bot, mutex):
    now = datetime.now()
    database = load_user_database(mutex)
    if now.weekday() == 6:
        if now.hour == 17:
            for user in database:
                if user["week_reminders"] == True:
                    bot.send_message(user["week_reminders"], "Done! You won't receive any reminder")
    else:
        time.sleep(60)

