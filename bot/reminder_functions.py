from datetime import datetime

from bot.markup import reminder_markup, start_markup
from bot.utility import save_to_user_database, load_user_database, load_lessons_database


def call_reminder(user_id, chat_id, mutex, bot):
    database = load_user_database(mutex)
    flag_w = database[str(user_id)]["weekly_reminders"]
    flag_d = database[str(user_id)]["daily_reminders"]
    bot.send_message(chat_id, "What do you want to do? \n\n"
                              "The weekly reminder will warn you every Sunday at 5pm to book the lessons "
                              "for the following week \n\nThe lesson reminder will warn you the day before "
                              "each lesson to remind you cancel it, if you are not going to attend\n\n"
                              "If you have already set a reminder you will have the option to disable it",
                     reply_markup=reminder_markup(flag_w, flag_d))


def manage_reminder(call, mutex, bot):
    database = load_user_database(mutex)
    chat_id = call.message.chat.id
    flag_w = database[str(call.from_user.id)]["weekly_reminders"]
    flag_d = database[str(call.from_user.id)]["daily_reminders"]

    if call.data == "rem_sw":
        flag_w = True
        bot.send_message(chat_id, "Done! You will receive a reminder every Sunday at 5pm\n\n"
                                  "Something else you want to do?", reply_markup=start_markup())
    elif call.data == "rem_sd":
        flag_d = True
        bot.send_message(chat_id, "Done! You will receive a reminder every day about the next day lessons "
                                  "booked using the bot\n\n "
                                  "Something else you want to do?", reply_markup=start_markup())
    elif call.data == "rem_sb":
        flag_w = True
        flag_d = True
        bot.send_message(chat_id, "Done! You will receive a reminder every Sunday at 5pm and "
                                  "every day about the next day lessons booked using the bot\n\n"
                                  "Something else you want to do?", reply_markup=start_markup())
    elif call.data == "rem_dw":
        flag_w = False
        bot.send_message(chat_id, "Done! You won't receive a weekly message\n\n"
                                  "Something else you want to do?", reply_markup=start_markup())
    elif call.data == "rem_dd":
        flag_d = False
        bot.send_message(chat_id, "Done! You won't receive a reminder before the lessons\n\n"
                                  "Something else you want to do?", reply_markup=start_markup())
    elif call.data == "rem_db":
        flag_w = False
        flag_d = False
        bot.send_message(chat_id, "Done! You won't receive any reminder\n\n"
                                  "Something else you want to do?", reply_markup=start_markup())

    database[str(call.from_user.id)]["weekly_reminders"] = flag_w
    database[str(call.from_user.id)]["daily_reminders"] = flag_d
    save_to_user_database(database, mutex)


def send_weekly_reminders(bot, mutex):
    database = load_user_database(mutex)
    for user in database:
        if database[user]["weekly_reminders"]:
            bot.send_message(database[user]["chat_id"], "Hey! Remember to book the lessons for next week!")


def send_daily_reminders(bot, mutex):
    now = datetime.now()
    database = load_user_database(mutex)
    lessons = load_lessons_database()
    day_num = {
        'Monday': 0,
        'Tuesday': 1,
        'Wednesday': 2,
        'Thursday': 3,
        'Friday': 4,
        'Saturday': 5,
        'Sunday': 6
    }
    for user in database:
        if database[user]["daily_reminders"]:
            to_remind = ""
            to_remove = []
            for lesson_val in database[user]["booked_lessons"]:
                lesson_dict = lessons[lesson_val[0:-1]]
                lesson = list(lesson_dict.values())[0][int(lesson_val[-1])]
                if (now.weekday() + 1) % 7 == day_num[lesson["day"]]:
                    to_remind.append(
                        "\n" + list(lesson_dict.keys())[0] + " " + lesson["day"] + " from " + lesson["from"] + " to " +
                        lesson["to"] + " in " +
                        lesson["room"].split("--")[0] + " " + lesson["building"])
                    to_remove.append(lesson_val)
            if to_remind != "":
                bot.send_message(user["chat_id"], "Hey! These are the lessons you have tomorrow:" + to_remind +
                                 "\n\nRemember to cancel if you are not attending.")
            for l in to_remove:
                database[user]["booked_lessons"].remove(l)
