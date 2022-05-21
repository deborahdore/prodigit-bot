import threading
import time

import requests

botoken = '5214072158:AAGj-lZig1CmTn06nI7JBiTH7nbm1grlv_I'
endpoint = 'https://api.telegram.org/bot' + botoken + '/'
message_buffer = []
last = 0
mutex = threading.Semaphore()


class Producer(threading.Thread):
    def run(self):
        global message_buffer
        global mutex
        global last

        mutex.acquire()
        messages = requests.get(endpoint + 'getUpdates').json()
        for i in range(len(messages['result'])):

            if int(messages['result'][i]['update_id']) > last:
                message_buffer.extend(messages['result'][i:])

                # update last
                last = message_buffer[-1]['update_id']

                break

        mutex.release()
        time.sleep(0.1)


class Consumer(threading.Thread):
    def run(self):
        global message_buffer
        global mutex

        mutex.acquire()

        if len(message_buffer) > 0:
            while len(message_buffer) != 0:
                message = message_buffer.pop(0)
                requests.post(
                    url=f'{endpoint}sendMessage',
                    data={'chat_id': message['message']['chat']['id'], 'text': 'hello friend'},

                )

        mutex.release()
        time.sleep(0.1)


if __name__ == '__main__':
    while True:
        # Creating Threads
        producer = Producer()
        consumer = Consumer()

        # Starting Threads
        consumer.start()
        producer.start()

        # Waiting for threads to complete
        producer.join()
        consumer.join()
