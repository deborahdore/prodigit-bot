from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def start_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(InlineKeyboardButton("Book", callback_data="/book"),
               InlineKeyboardButton("Reminder", callback_data="/reminders"))
    return markup
