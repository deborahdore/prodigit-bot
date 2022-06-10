import json
from json import JSONDecodeError
from threading import Semaphore

from requests.structures import CaseInsensitiveDict

USER_DATABASE = "database/user-database.json"
LESSON_DATABASE = "database/lesson-database.json"


def load_user_database(mutex: Semaphore):
    mutex.acquire()
    try:
        db = json.load(open(USER_DATABASE, "r"))
        mutex.release()
    except JSONDecodeError:
        with open(USER_DATABASE, "w") as outfile:
            outfile.write(json.dumps({}, indent=4))
        mutex.release()
        return json.load(open(USER_DATABASE))
    return db


def save_to_user_database(database, mutex: Semaphore):
    mutex.acquire()
    json.dump(database, open(USER_DATABASE, "w"))
    mutex.release()


def create_headers(cookie=None):
    headers = CaseInsensitiveDict()
    headers[
        "Accept"] = "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"
    headers["Connection"] = "keep-alive"
    headers["Content-Type"] = "application/x-www-form-urlencoded"
    if cookie is not None:
        headers['Cookie'] = cookie
    return headers


def load_lessons_database():
    db = json.load(open(LESSON_DATABASE, "r"))
    return db
