#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This program is dedicated to the public domain under the CC0 license.

from django.core.management.base import BaseCommand
from django.conf import settings
from .print import do_print
from .bases import profile, write_to_category, read_from_base
from telegram import Update, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, Filters, MessageHandler, ConversationHandler
from .keyboards import get_buttons, get_keyboard_category, CATEGORIES, DEL_CATEGORY, NEW_CATEGORY

# P = ""  # Variable 'p' for ask 'Profile'. Temporarily.
START, ASK = range(2)
data_from_base_categories = []


def log_errors(f):

    def inner(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            error_message = f'Ошибка: {e}___{f}'
            print(error_message)
            raise e
    return inner


@log_errors
def get_profile(update):
    chat_id = update.message.chat_id
    p, _ = profile(update, chat_id)
    return p, _


@log_errors
def try_handler(update, context):
    p, _ = get_profile(update)
    if not _:
        update.message.reply_text(text='С Возвращением!\nВыберите кнопки:', reply_markup=get_keyboard_category())
        return START
    else:
        text = 'Добро пожаловать!\nВыберите категорию знаний, которые вы будите закреплять'
        update.message.reply_text(text=text, reply_markup=get_keyboard_category())
        return START


@log_errors
def start_categories(update, context):
    global data_from_base_categories
    text = update.message.text
    p, _ = get_profile(update)
    if text == CATEGORIES:
        categories = read_from_base(p)
        data_from_base_categories = []
        for i in categories:
            data_from_base_categories.append(str(i))
        print(data_from_base_categories, type(data_from_base_categories))
        reply_markup = get_buttons(data_from_base_categories)
        update.message.reply_text(text='Выберете одну из категорий:', reply_markup=reply_markup)
    elif text == NEW_CATEGORY:
        update.message.reply_text('Введите название новой категории:', reply_markup=ReplyKeyboardRemove())
        return ASK
    elif text == DEL_CATEGORY:
        pass
    else:
        update.message.reply_text('Выберите нужное действие внизу:', reply_markup=get_keyboard_category())


@log_errors
def ask_handler(update, category_data: dict):
    category_name = update.message.text
    p, _ = get_profile(update)
    write_to_category(p=p, text=category_name)
    update.message.reply_text('Записали!', reply_markup=get_keyboard_category())
    return ConversationHandler.END


@log_errors
def cancel(update: Update):
    """
    Отменить весь процесс диалога. Данные будут утеряны
    """
    if update.message.text == "/cancel":
        update.message.reply_text("Отмена. Для начала с нуля нажмите /start")
        return ConversationHandler.END


@log_errors
def button_inline(update, context):
    query = update.callback_query
    data = query.data
    query.answer()

    if data in data_from_base_categories:
        query.edit_message_text(text=data, reply_markup=ReplyKeyboardRemove())
    if data == '1':
        text = f'Считать категории из бызы!'
        query.edit_message_text(text=text)  # "Selected option: {}".format(query.data)
    elif data == '2':
        pass
    elif data == '3':
        pass


@log_errors
def do_start(update, context):
    pass


@log_errors
def help(update, context):
    update.message.reply_text("Use /start to test this bot.")


@log_errors
def main():
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(token=settings.TG_TOKEN, base_url=settings.TG_PROXY_URL, use_context=True)

    con_handler = ConversationHandler(
        entry_points=[
            CommandHandler("start", try_handler)
        ],
        states={
            START: [
                MessageHandler(Filters.all, start_categories, pass_user_data=True)  # pass_user_data -
                # прокидывает данные из одной функции в другую
            ],
            ASK: [
                MessageHandler(Filters.all, ask_handler, pass_user_data=True)
            ],
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )
    updater.dispatcher.add_handler(con_handler)
    updater.dispatcher.add_handler(CommandHandler('start_OLD', do_start))
    updater.dispatcher.add_handler(CallbackQueryHandler(button_inline))
    updater.dispatcher.add_handler(CommandHandler('help', help))
    # updater.dispatcher.add_error_handler(error)
    updater.dispatcher.add_handler(MessageHandler(Filters.text, do_print))

    # Start the Bot
    updater.start_polling()

    # Run the bot until the user presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT
    updater.idle()


@log_errors
class Command(BaseCommand):
    help = 'Телеграм-бот'

    def handle(self, *args, **options):
        main()


if __name__ == '__main__':
    с = Command()
    с
