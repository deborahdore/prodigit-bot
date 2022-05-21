import logging
import requests as re
from telegram import *
from telegram.ext import filters, MessageHandler, ApplicationBuilder, CommandHandler, CallbackContext


"""logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: CallbackContext.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")

async def rispondimale(update: Update, context: CallbackContext.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="we...a fess' e mammt'!")

async def book(update: Update, context: CallbackContext.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id,text="Che cosa vorresti prenotare?")

if __name__ == '__main__':
    application = ApplicationBuilder().token('5214072158:AAGj-lZig1CmTn06nI7JBiTH7nbm1grlv_I').build()



    echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), rispondimale)
    buttons = ['Start', 'Settings', 'Back']
    markup = ReplyKeyboardMarkup.from_column(buttons)
    MessageHandler(filters.Text(buttons), book)
    
    start_handler = CommandHandler('hi', start)
    application.add_handler(start_handler)
    application.add_handler(CommandHandler('strunz', rispondimale))
    application.add_handler(CommandHandler('book', book))
               
    application.run_polling()"""

botoken='5214072158:AAGj-lZig1CmTn06nI7JBiTH7nbm1grlv_I'
endpoint = 'https://api.telegram.org/bot'+botoken+'/'
initbot = re.get(endpoint+'getme')
last = 0

def update():
    messages = re.get(endpoint+'getUpdates').json()
    for i in range(messages['result']):
        if(messages['result'][i]['update_id'] > last):
            last = messages['result'][i]['update_id']
            return messages['result'][i:]

if __name__ == '__main__':
    messages = []
    while True:
        if(len(messages)==0):
            messages.append(update)

        if(len(messages)!=0):
            for i in messages:
                messages.remove(i)

#print(initbot.json())