import re

from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton


def start_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(InlineKeyboardButton("Book", callback_data="/book"),
               InlineKeyboardButton("Reminder", callback_data="/reminders"))
    return markup


def save_credentials_markup():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add(KeyboardButton("Yes"),
               KeyboardButton("No"))
    return markup


def create_lessons_markups(lesson, lesson_id):
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    for i in range(0, len(lesson)):
        if i > 7:
            break
        markup.add(InlineKeyboardButton("Yes on " + lesson[i]["day"], callback_data="/n_l_" + lesson_id + str(i)))
    markup.add(InlineKeyboardButton("All", callback_data="/n_l_!all_" + lesson_id))
    markup.add(InlineKeyboardButton("No", callback_data="/n_l_!no"))
    return markup


def user_lessons_markups(user_lessons, lessons):
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    all_lessons = ""
    for i in range(0, len(user_lessons)):
        day = lessons[user_lessons[i][:-1]][list(lessons[user_lessons[i][:-1]].keys())[0]][int(
            user_lessons[i][-1])]["day"]
        markup.add(InlineKeyboardButton(list(lessons[user_lessons[i][:-1]].keys())[0].lower().capitalize() + " on " +
                                        day,
                                        callback_data="/l_" + user_lessons[i]))
        all_lessons = all_lessons + "_" + user_lessons[i]
    markup.add(InlineKeyboardButton("All", callback_data="/l_all" + all_lessons))
    return markup


def confirm_book_markup(call, lessons):
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    if re.match("^/n_l", call):
        if re.match("^\d", call.split("_")[2]):
            lesson = call.split("_")[2]
            markup.add(InlineKeyboardButton("Yes", callback_data="/bk_n_" + lesson))
        elif re.match("^!all", call.split("_")[2]):
            lesson_list = ""
            name = call.split("_")[3]
            for i in range(0, len(lessons[name][list(lessons[name].keys())[0].upper()])):
                lesson_list = lesson_list + "_" + name + str(i)
            markup.add(InlineKeyboardButton("Yes", callback_data="/bk_n" + lesson_list))
    elif re.match("^/l_all", call):
        callback_data = call.replace("l_all", "bk")
        markup.add(InlineKeyboardButton("Yes", callback_data=callback_data))
    elif re.match("^/l_", call):
        callback_data = call.replace("l", "bk")
        markup.add(InlineKeyboardButton("Yes", callback_data=callback_data))

    markup.add(InlineKeyboardButton("No", callback_data="/bk_no"))
    return markup


def confirm_save_lesson_markup(lesson):
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(InlineKeyboardButton("Yes", callback_data="/s_l" + lesson))
    markup.add(InlineKeyboardButton("No", callback_data="/s_no"))
    return markup
