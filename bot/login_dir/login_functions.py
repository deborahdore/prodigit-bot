from datetime import datetime, timedelta

from bot.login_dir.login import login
from bot.markup import save_credentials_markup, user_lessons_markups
from bot.utility import load_user_database, save_to_user_database


def user_exist(id_telegram, mutex):
    database = load_user_database(mutex)
    return str(id_telegram) in database


def check_if_we_have_credentials(id_telegram, mutex):
    database = load_user_database(mutex)[str(id_telegram)]
    is_logged = database['login']
    saved_lessons = database['saved_lessons']
    if is_logged is False:
        # check for token
        if database['token'] is not "":
            # check for timestamp
            now = datetime.now()
            if (now - timedelta(hours=2)) <= datetime.strptime(database['timestamp_token'], '%Y-%m-%d %H:%M:%S') <= now:
                # we took the token less than 2 hour ago
                is_logged = True
    return is_logged, saved_lessons


def call_booking_request(user_id, chat_id, mutex, bot, phases, lessons):
    assert user_exist(user_id, mutex)
    credentials_check = check_if_we_have_credentials(user_id, mutex)

    if credentials_check[0]:
        if credentials_check[1]:
            bot.send_message(chat_id, "Write the name of the course you want to book for "
                                      "or choose a lesson which you have already booked.",
                             reply_markup=user_lessons_markups(credentials_check[1], lessons))
            phases[chat_id] = "waiting for lesson name"
        else:
            bot.send_message(chat_id, "Write the name of the course you want to book for.")
            phases[chat_id] = "waiting for lesson name"
    else:
        # senza credenziali
        phases[chat_id] = "waiting for matricola"

        bot.send_message(chat_id, "First of all you need to insert your credentials."
                                  "It will only be used to access Prodigit, and you can choose to delete them afterwards.\n\n"
                                  "Please write your student ID (matricola)")


def insert_matricola(message, mutex, bot, phases):
    database = load_user_database(mutex)
    database[str(message.from_user.id)]['matricola'] = message.text
    save_to_user_database(database, mutex)

    bot.send_message(message.chat.id, "Now insert your password")
    phases[message.chat.id] = "waiting for password"


def insert_password(message, mutex, bot, phases):
    id_telegram = str(message.from_user.id)

    database = load_user_database(mutex)

    password = message.text

    token = login(database[id_telegram]['matricola'], password)
    if token is not "":
        database[id_telegram]['password'] = password
        database[id_telegram]['token'] = token
        save_to_user_database(database, mutex)
        bot.send_message(message.chat.id, "You have logged in correctly. \n"
                                          "Do you want to save your credentials?\n",
                         reply_markup=save_credentials_markup())
        phases[message.chat.id] = "waiting for save credentials"
    else:
        bot.send_message(message.chat.id, "Incorrect credentials. Re-enter your matricola")
        phases[message.chat.id] = "waiting for matricola"


def save_credentials(message, mutex, bot, phases, lessons):
    id_telegram = str(message.from_user.id)
    database = load_user_database(mutex)
    if message.text == "Yes":
        database[id_telegram]['login'] = True

    elif message.text == "No":
        database[id_telegram]['matricola'] = ""
        database[id_telegram]['password'] = ""

    save_to_user_database(database, mutex)

    if len(database[id_telegram]["saved_lessons"]) == 0:
        bot.send_message(message.chat.id, "Okay! All good!\n"
                                          "Write the name of the course you want to book for.")
    else:
        bot.send_message(message.chat.id, "Okay! All good!\n"
                                          "Write the name of the course you want to book for or choose a lesson which "
                                          "you have already booked.",
                         reply_markup=user_lessons_markups(database[id_telegram]["saved_lessons"], lessons))
    phases[message.chat.id] = "waiting for lesson name"
