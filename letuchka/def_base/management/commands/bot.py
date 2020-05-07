#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand
from django.conf import settings
from .bases import profile, write_to_category, read_from_category, delete_category
from telegram import Update, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, Filters, MessageHandler
from .keyboards import get_buttons_category, get_keyboard_into


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
class Command(BaseCommand):
    help = 'Телеграм-бот'
    data_add = None
    global_chat_id = None
    selected_category = None

    @log_errors
    def do_start(self, update, context):
        self.global_chat_id = update.message.chat_id
        p, _ = profile(update, self.global_chat_id)
        reply_markup = get_buttons_category(read_from_category(p))
        if not _:
            update.message.reply_text(text='С Возвращением!\nВыберите Категорию:', reply_markup=reply_markup)
        else:
            text = 'Добро пожаловать!\nВыберите Категорию знаний, которые вы будите закреплять'
            update.message.reply_text(text=text, reply_markup=reply_markup)

    @log_errors
    def do_print(self, update, context):
        print('print')
        self.global_chat_id = update.message.chat_id
        p, _ = profile(update, self.global_chat_id)
        print(p)
        if self.data_add == '__<ADD>__':
            write_to_category(p, update.message.text)
            reply_markup = get_buttons_category(read_from_category(p))
            text = f'Добавлена Категория "{update.message.text}"\n\nВыберите Категорию'
            update.message.reply_text(text=text, reply_markup=reply_markup)
        else:
            update.message.reply_text(update.message.text)

    @log_errors
    def button_inline(self, update: Update, context):
        print('button_inline')
        query = update.callback_query
        self.data_add = query.data
        query.answer()
        p, _ = profile(update, update.effective_message.chat_id)

        if query.data == '__<ADD>__':
            # Press button Add
            text = 'Введите название новой Категории:'
            query.edit_message_text(text=text)

        elif query.data in [str(i) for i in read_from_category(p)] and query.data != '__<ADD>__':
            # Press a Category
            self.selected_category = query.data
            text = f'Выбрана Категория "{self.selected_category}"\n\nВыберите кнопки:'
            buttons_into_category = get_keyboard_into([
                'Определения',
                'Настройка',
                'Удалить',
                'Назад'
            ])
            query.edit_message_text(text=text, reply_markup=buttons_into_category)

        elif self.selected_category and query.data == 'Удалить':
            # Press button Add
            delete_category(p, self.selected_category)
            text = 'Категория удалена.\n\nВыберете Категорию:'
            reply_markup = get_buttons_category(read_from_category(p))
            query.edit_message_text(text=text, reply_markup=reply_markup)
        else:
            reply_markup = get_buttons_category(read_from_category(p))
            query.edit_message_text(text=f'Думай!\n\n{query.data}', reply_markup=reply_markup)

    @log_errors
    def cancel(self, update, context):
        # user = update.message.from_user
        # logger.info("User %s canceled the conversation.", user.first_name)
        update.message.reply_text('Bye! I hope we can talk again some day.')  # reply_markup=ReplyKeyboardRemove())

    @log_errors
    def handle(self, *args, **options):
        updater = Updater(token=settings.TG_TOKEN, base_url=settings.TG_PROXY_URL, use_context=True)

        updater.dispatcher.add_handler(CommandHandler('start', self.do_start))
        updater.dispatcher.add_handler(CommandHandler('cancel', self.cancel))
        updater.dispatcher.add_handler(CallbackQueryHandler(self.button_inline))
        updater.dispatcher.add_handler(MessageHandler(Filters.text, self.do_print))

        # Start the Bot
        updater.start_polling()

        # Run the bot until the user presses Ctrl-C or the process receives SIGINT,
        # SIGTERM or SIGABRT
        updater.idle()


if __name__ == '__main__':
    с = Command()
    с
