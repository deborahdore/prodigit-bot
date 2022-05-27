import re
import urllib
from datetime import datetime

import requests

from bot.markup import start_markup
from bot.utility import load_user_database, create_headers

BOOKING_URL = "https://prodigit.uniroma1.it/prenotazioni/prenotaaule.nsf/prenotaposto-aula-lezioni"

WEEKDAY_TO_NUM = {
    'Monday': 0,
    'Tuesday': 1,
    'Wednesday': 2,
    'Thursday': 3,
    'Friday': 4,
    'Saturday': 5,
    'Sunday': 6
}
LAST_WEKDAY: int = WEEKDAY_TO_NUM['Sunday']
CLICK_URL: str = 'https://prodigit.uniroma1.it/prenotazioni/prenotaaule.nsf/' \
                 'prenotaposto-aula-lezioni?OpenForm&Seq=4#_RefreshKW_dichiarazione'


def find_day(day_of_week):
    current_day: int = datetime.today().weekday()
    day_offset: int = LAST_WEKDAY - current_day + 1
    days_from_now: int = WEEKDAY_TO_NUM[day_of_week] + day_offset

    if days_from_now > 10:
        print(f'unable to book class for {day_of_week}')
        return -1
    return days_from_now


def find_click_magic(headers):
    click_data = urllib.parse.urlencode([
        ('__Click', '$Refresh'),
        ('codiceedificio', 'AOSG1'),
        ('aula', 'AULA 3 ESTERNA -- AOSG1-0003'),
        ('dalleore1', '08:00'),
        ('alleore1', '09:00'),
        ('dichiarazione', ':'),  # this does the trick!
    ]).encode()

    click_resp = requests.post(CLICK_URL, headers=headers, data=click_data)

    return re.search("return _doClick\('(.+)', this, null\)",
                     click_resp.text).group(1)


def create_params(click_magic, cod_edificio, room, giorno, from_hour, to_hour):
    day = find_day(giorno)

    data = urllib.parse.urlencode([
        ('__Click', click_magic),
        ('codiceedificio', cod_edificio),
        ('aula', room),
        ('dalleore' + str(day), from_hour),
        ('alleore' + str(day), to_hour),
        ('dichiarazione', ':'),  # this does the trick!
    ]).encode()
    return data


def booking_request(lesson, mutex, bot, lessons, call, phases):
    lesson = lesson[0:-1]
    lesson_number = lesson[-1]

    lesson_dict = lessons[lesson]
    lesson = list(lesson_dict.values())[0][int(lesson_number)]

    headers = create_headers(load_user_database(mutex)[str(call.from_user.id)]['token'])

    params = create_params(find_click_magic(headers), lesson['building'], lesson['room'], lesson['day'], lesson['from'],
                           lesson['to'])

    resp = requests.post(BOOKING_URL, headers=headers,
                         data=params)

    if re.match(".*ERROR.*", resp.text):
        bot.send_message(call.message.chat.id, "Your booking wasn't confirmed. Try again\n"
                                               "1. Book a lecture \n"
                                               "2. Manage reminders", reply_markup=start_markup())
        phases[call.message.chat.id] = "start"

        raise Exception("Booking unconfirmed")
