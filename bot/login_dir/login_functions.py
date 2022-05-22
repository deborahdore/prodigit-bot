from bot.login_dir.login import login
from bot.markup import start_markup
from bot.utility import load_user_database, save_to_user_database


def user_exist(id_telegram, mutex):
    database = load_user_database(mutex)
    return str(id_telegram) in database


def check_if_we_have_credentials(id_telegram, mutex):
    database = load_user_database(mutex)
    return database[str(id_telegram)]['login']


def call_booking_request(call, mutex, bot, phases):
    assert user_exist(call.from_user.id, mutex)

    if check_if_we_have_credentials(call.from_user.id, mutex):
        bot.send_message(call.message.chat.id, "Write the name of the course you want to book for.")
        phases[call.message.chat.id] = "waiting for lesson name"
    else:
        # senza credenziali
        phases[call.message.chat.id] = "waiting for matricola"

        bot.send_message(call.message.chat.id, "First of all you need to insert your credentials."
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
                                          "Do you want to save your credentials?\n Yes/No/Cancel")
        phases[message.chat.id] = "waiting for save credentials"
    else:
        bot.send_message(message.chat.id, "Incorrect credentials. Re-enter your matricola")
        phases[message.chat.id] = "waiting for matricola"


def save_credentials(message, mutex, bot, phases):
    id_telegram = str(message.from_user.id)
    database = load_user_database(mutex)
    if message.text == "Yes":
        database[id_telegram]['login'] = True

    elif message.text == "No":
        database[id_telegram]['matricola'] = ""
        database[id_telegram]['password'] = ""

    else:
        phases[message.chat.id] = "start"
        bot.send_message(message.chat.id,
                         "What do you want to do?:\n"
                         "1. Book a lecture \n"
                         "2. Manage reminders", reply_markup=start_markup())

    save_to_user_database(database, mutex)
    bot.send_message(message.chat.id,  "Okay! All good! \n Write the name of the course you want to book for")
    phases[message.chat.id] = "waiting for lesson name"
