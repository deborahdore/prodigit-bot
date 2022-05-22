from bot.utility import load_lessons_database
from bot.markup import create_lessons_markups

def booking_known_lesson_request(message, mutex, bot, phases):
    print("credentials okay")
    #inserire parte di prenotazione
    bot.send_message(message.chat.id,"Booked!")
    phases[message.chat.id] = "start"

def booking_fork(message,mutex,bot,phases):
    lessons = find_lesson(message,mutex)
    if lessons == '0':
        bot.send_message(message.chat.id, "Sorry I cannot find your lesson")
    else:
        bot.send_message(message.chat.id, "You want to book for: " + lessons[0] + "?",
                         reply_markup=create_lessons_markups(lessons[0], lessons[1]))


def booking_request(lesson):
    print("sto prenotando...")
    pass

def find_lesson(message,mutex):
    lessons = load_lessons_database(mutex)

    for lesson in lessons["lessons"]:
        if lesson.lower().find(message.text.lower()) != -1:
            return lesson.lower().capitalize(), lessons["lessons"][lesson]
    return "0"