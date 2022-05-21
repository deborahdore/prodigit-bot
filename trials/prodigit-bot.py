import telebot

bot = telebot.TeleBot("5214072158:AAGj-lZig1CmTn06nI7JBiTH7nbm1grlv_I")


# Handles all text messages that contains the commands '/start' or '/help'.
@bot.message_handler(commands=['start', 'help'])
def handle_start_help(message):
    bot.send_message(message.chat.id,
                     "Hello! I'm a Bot made to make the life of Sapienza' student easy. Here's a list of what you can do:\n"
                     "1. Book a lecture \n"
                     "2. Manage reminders")


# Handles all sent documents and audio files
@bot.message_handler(content_types=['document', 'audio'])
def handle_docs_audio(message):
    pass


# Handles all text messages that match the regular expression
@bot.message_handler(regexp="/book")
def handle_message(message):
    bot.send_message(message.chat.id,
                     "book")


@bot.message_handler(regexp="/reminder")
def handle_message(message):
    bot.send_message(message.chat.id,
                     "reminder")


# Handles all messages for which the lambda returns True
@bot.message_handler(func=lambda message: message.document.mime_type == 'text/plain', content_types=['document'])
def handle_text_doc(message):
    pass


# Which could also be defined as:
def test_message(message):
    return message.document.mime_type == 'text/plain'


@bot.message_handler(func=test_message, content_types=['document'])
def handle_text_doc(message):
    pass


# Handlers can be stacked to create a function which will be called if either message_handler is eligible
# This handler will be called if the message starts with '/hello' OR is some emoji
@bot.message_handler(commands=['hello'])
@bot.message_handler(func=lambda msg: msg.text.encode("utf-8") == "")
def send_something(message):
    pass


if __name__ == '__main__':
    bot.infinity_polling(interval=0, timeout=20)
