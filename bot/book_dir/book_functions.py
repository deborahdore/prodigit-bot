import re

from bot.login_dir.login_functions import call_booking_request
from bot.markup import create_lessons_markups, confirm_book_markup, start_markup
from bot.utility import load_user_database, save_to_user_database


def booking_new_lesson(message, bot, phases, lessons):
    found_lessons = find_lesson(message, lessons)
    if found_lessons == '0':
        bot.send_message(message.chat.id, "Sorry I cannot find your lesson, could you please try again?")
    else:
        bot.send_message(message.chat.id, "You want to book for: " + found_lessons[0] + "?",
                         reply_markup=create_lessons_markups(found_lessons[1], found_lessons[2]))
        phases[message.chat.id] = "waiting to book"


def recap(call, bot, phases, lessons):
    if re.match("^/n_l", call.data):
        if re.match("^!all", call.data.split("_")[2]):
            lesson = list(lessons[call.data.split("_")[3]].keys())[0]
            bot.send_message(call.message.chat.id, "Here's a Recap!:\n" + lesson.lower().capitalize() +
                             " for each day of lessons of this week.\n Do you confirm your reservations?",
                             reply_markup=confirm_book_markup(call.data, lessons))
        elif re.match("^\d", call.data.split("_")[2]):
            pos = int(call.data[-1])
            lesson = lessons[call.data.split("_")[2][:-1]][list(lessons[call.data.split("_")[2][:-1]].keys())[0]]
            name = list(lessons[call.data.split("_")[2][:-1]].keys())[0].lower().capitalize()
            bot.send_message(call.message.chat.id, "Here's a Recap!:\n" + name + " on " + lesson[pos]["day"]
                             + "\nfrom " + lesson[pos]["from"] + " to " + lesson[pos]["to"] +
                             " in " + lesson[pos]["room"].split("--")[0] + ", " + lesson[pos]["building"] +
                             ".\n Do you confirm your reservation?",
                             reply_markup=confirm_book_markup(call.data, lessons))
        elif re.match("/n_l_!no", call.data):
            phases[call.message.chat.id] = "start"
            bot.send_message(call.message.chat.id,
                             "What would you like to do?\n"
                             "1. Book a lecture \n"
                             "2. Manage reminders", reply_markup=start_markup())
    elif re.match("^/l_", call.data):
        if re.match("^all", call.data.split("_")[1]):
            bot.send_message(call.message.chat.id, "Would you like to book all saved reservations?",
                             reply_markup=confirm_book_markup(call.data, lessons))
        else:
            pos = int(call.data[-1])
            lesson = lessons[call.data.split("_")[1][:-1]][list(lessons[call.data.split("_")[1][:-1]].keys())[0]]
            name = list(lessons[call.data.split("_")[1][:-1]].keys())[0].lower().capitalize()
            bot.send_message(call.message.chat.id, "Here's a Recap!:\n" + name + " on " + lesson[pos]["day"]
                             + "\nfrom " + lesson[pos]["from"] + " to " + lesson[pos]["to"] +
                             " in " + lesson[pos]["room"].split("--")[0] + ", " + lesson[pos]["building"] +
                             ".\n Do you confirm your reservation?",
                             reply_markup=confirm_book_markup(call.data, lessons))


def find_lesson(message, lessons):
    for lesson in lessons:
        if list(lessons[lesson].keys())[0].lower().find(message.text.lower()) != -1:
            # 0.Name of the lesson 1.Body 2.ID
            return list(lessons[lesson].keys())[0].lower().capitalize(), \
                   lessons[lesson][list(lessons[lesson].keys())[0]], lesson
    return "0"


def save_lesson(call, mutex, lessons):
    id_telegram = str(call.from_user.id)
    database = load_user_database(mutex)

    if re.match("^/s_l", call.data):
        lesson_saved = call.data.split("_")
        for i in range(2, len(call.data.split("_"))):
            lesson_i = lesson_saved[i]
            if lesson_i not in database[id_telegram]["saved_lessons"]:
                database[id_telegram]["saved_lessons"].insert(0, lesson_i)
            else:
                l_index = database[id_telegram]["saved_lessons"].index(lesson_i)
                database[id_telegram]["saved_lessons"].pop(l_index)
                database[id_telegram]["saved_lessons"].insert(0, lesson_i)

    save_to_user_database(database, mutex)


def message_booking_request(message, mutex, bot, phases, lessons):
    phases[message.chat.id] = "book"
    call_booking_request(message.from_user.id, message.chat.id, mutex, bot, phases, lessons)
