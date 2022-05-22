import re

import telebot
import json
import ast
import time
from telebot import types

bot = telebot.TeleBot("5214072158:AAGj-lZig1CmTn06nI7JBiTH7nbm1grlv_I")

# Stats { 1:Book , 2: reminders , 3:Log , 4: not in Mode }
active_users = {}


@bot.message_handler(regexp="^[a-zA-Z]")
def free_message_handler(message):
    if message.chat.id in active_users:
        if active_users[message.chat.id] == 1:
            active_users[message.chat.id] = 4
            lesson = find_lesson(message.text)
            if lesson == '0':
                bot.send_message(message.chat.id, "Sorry I cannot find your lesson")
            else:
                bot.send_message(message.chat.id, "You want to book for: " + lesson[0] + "?",
                                 reply_markup=create_lessons_bottom(lesson[0],lesson[1]))


# Handles all text messages that contains the commands '/start' or '/help'.
@bot.message_handler(commands=['start', 'help'])
def handle_start_help(message):
    bot.send_message(message.chat.id,
                     "Hello! I'm a Bot made to make the life of Sapienza' student easy. Here's a list of what you can do:\n"
                     "1. Book a lecture \n"
                     "2. Manage reminders")


# Handles all text messages that match the regular expression
@bot.message_handler(commands=["book"])
def handle_message(message):
    active_users[message.chat.id] = 1
    bot.send_message(message.chat.id,
                     "Write the name of the lesson you want to book a seat for")


@bot.message_handler(regexp="/reminder")
def handle_message(message):
    bot.send_message(message.chat.id,
                     "reminder")


@bot.callback_query_handler(func=lambda call:re.match("cb_*", call.data))
def callback_query(call):
    chat_id = call.message.chat.id
    if call.data == "cb_1":
        bot.send_message(chat_id, "YES")
    elif call.data == "cb_no":
        bot.send_message(chat_id, "NO!")


'''
# Handles all sent documents and audio files
@bot.message_handler(content_types=['document', 'audio'])
def handle_docs_audio(message):
    pass

# Handles all messages for which the lambda returns True
@bot.message_handler(func=lambda message: message.document.mime_type == 'text/plain', content_types=['document'])
def handle_text_doc(message):
    pass


# Which could also be defined as:
def test_message(message):
    return message.document.mime_type == 'text/plain'


@bot.message_handler(func=test_message, content_types=['document'])
def handle_text_doc(message):
    pass


# Handlers can be stacked to create a function which will be called if either message_handler is eligible
# This handler will be called if the message starts with '/hello' OR is some emoji
@bot.message_handler(commands=['hello'])
@bot.message_handler(func=lambda msg: msg.text.encode("utf-8") == "")
def send_something(message):
    pass

'''


def create_lessons_bottom(name,lessons):
    markup = telebot.types.InlineKeyboardMarkup()
    markup.row_width = 1
#    all = name
    for i in range(0, len(lessons)):
        markup.add(telebot.types.InlineKeyboardButton("Yes on " + lessons[i]["day"], callback_data="cb_" + str(i)))
                                                      #+";"+name+";"+lessons[i]["building"]+";"+lessons[i]["room"]+
                                                      #";"+lessons[i]["day"]+";"+lessons[i]["from"]+";"+lessons[i]["to"]))
        #all = all + "[" + lessons[i]["building"] + ";" + lessons[i]["room"] + ";" + lessons[i]["day"] + ";"\
              #+ lessons[i]["from"] + ";" + lessons[i]["to"]+"]"'''
    markup.add(telebot.types.InlineKeyboardButton("All", callback_data="cb_all"))
    markup.add(telebot.types.InlineKeyboardButton("No", callback_data="cb_wrong"))
    return markup


def find_lesson(name):
    f = open("../database/database.json")
    lessons = json.load(f)
    f.close()

    for lesson in lessons["lessons"]:
        if lesson.lower().find(name.lower()) != -1:
            return lesson.lower().capitalize(), lessons["lessons"][lesson]
    return "0"


if __name__ == '__main__':
    bot.infinity_polling(interval=0, timeout=20)
