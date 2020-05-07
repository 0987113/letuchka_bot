from subprocess import Popen
from subprocess import PIPE

from telegram import Bot
from telegram import Update
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler
from telegram.ext import Filters

TG_TOKEN = ''
TG_API_URL = ''


def do_start(bot: Bot, update: Update):
    bot.send_message(
        chat_id=update.message.chat_id,
        text="Hello world",
    )


def do_print(bot: Bot, update: Update):
    chat_id = update.message.chat_id  # chat_id - id человека который нам написал
    text = "Ваш ID = {}\n\n{}".format(chat_id, update.message.text)
    # user_id = update.message.user_id

    bot.send_message(
        chat_id=update.message.chat_id,
        text=text,
    )


def do_help(bot: Bot, update: Update):
    print("do_help")
    bot.send_message(
        chat_id=update.message.chat_id,
        text="Это учебный бот\n"
             "Список учебных команд в меню\n\n"
             "Так же я отвечу на любое сообщение",
    )


def do_time(bot: Bot, update: Update):
    print("do_time")
    """
    process = Popen(["date"], stdout = PIPE)
    text, error = process.communicate()
    print(text.decode("utf-8"))
    if error:
        print("if")
        text = "Произошла ошибка, время неизвестно"
    else: 
        print("else")
        text = text.decode("utf-8")
    """
    """code = subprocess.call(["date"], stdout=PIPE)
    print(stdout)"""
    text = "time"
    bot.send_message(
        chat_id=update.message.chat_id,
        text=text,
    )


def main():
    bot = Bot(token=TG_TOKEN, base_url=TG_API_URL)
    updater = Updater(bot=bot)

    time_handler = CommandHandler("time", do_time)
    help_handler = CommandHandler("help", do_help)
    start_handler = CommandHandler("start", do_start)
    message_handler = MessageHandler(Filters.text, do_print)

    updater.dispatcher.add_handler(time_handler)
    updater.dispatcher.add_handler(help_handler)
    updater.dispatcher.add_handler(start_handler)
    updater.dispatcher.add_handler(message_handler)
    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()

