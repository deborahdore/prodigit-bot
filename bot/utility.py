import json
from threading import Semaphore


def load_user_database(mutex: Semaphore):
    mutex.acquire()
    db = json.load(open("../database/user-database.json"))
    mutex.release()
    return db


def save_to_user_database(database, mutex: Semaphore):
    mutex.acquire()
    json.dump(database, open("../database/user-database.json", "w"))
    mutex.release()
