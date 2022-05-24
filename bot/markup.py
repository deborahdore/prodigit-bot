from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from bot.utility import load_user_database, save_to_user_database

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


def reminder_markup(flag_w, flag_d):
    bell = u'\U0001F514'
    not_bell = u'\U0001F515'
    markup = InlineKeyboardMarkup()
    if flag_w:
        btn_w = InlineKeyboardButton("disable weekly reminder " + not_bell, callback_data="rem_dw")
    else:
        btn_w = InlineKeyboardButton("set weekly reminder " + bell, callback_data="rem_sw")
    if flag_d:
        btn_d = InlineKeyboardButton("disable lesson reminder " + not_bell, callback_data="rem_dd")
    else:
        btn_d = InlineKeyboardButton("set lesson reminder " + bell, callback_data="rem_sd")
    btn_eb = InlineKeyboardButton("set both " + bell, callback_data="rem_sb")
    btn_db = InlineKeyboardButton("disable both " + not_bell, callback_data="rem_db")
    markup.row(btn_w)
    markup.row(btn_d)
    markup.row(btn_eb, btn_db)
    return markup