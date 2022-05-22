from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

from bot.utility import load_user_database


def start_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(InlineKeyboardButton("Book", callback_data="/book"),
               InlineKeyboardButton("Reminder", callback_data="/reminders"))
    return markup

def create_lessons_markups(name,lessons):
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    all = name
    for i in range(0, len(lessons)):
        markup.add(InlineKeyboardButton("Yes on " + lessons[i]["day"], callback_data="/new_lesson" + str(i)
                                                      +";"+name+";"+lessons[i]["building"]+";"+lessons[i]["room"]+
                                                      ";"+lessons[i]["day"]+";"+lessons[i]["from"]+";"+lessons[i]["to"]))
        all = all + "[" + lessons[i]["building"] + ";" + lessons[i]["room"] + ";" + lessons[i]["day"] + ";"\
              + lessons[i]["from"] + ";" + lessons[i]["to"]+"]"
    markup.add(InlineKeyboardButton("All", callback_data="/new_lesson_all"))
    markup.add(InlineKeyboardButton("No", callback_data="/new_lesson_no"))
    return markup

def user_lessons_markups(user,mutex):
    db = load_user_database(mutex)
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    lessons = db[user]["saved_lessons"]
    for i in range(0, len(lessons)):
        markup.add(InlineKeyboardButton(lessons[i][0]+" on "+lessons[i][3],
                                        callback_data="/lesson"+i))
    markup.add(InlineKeyboardButton("All","/lessonAll"))
    return markup,lessons

