#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand
from django.conf import settings
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, Filters, MessageHandler
from .keyboards import get_buttons_cd, get_keyboard_into
from .buttons_handler import validate_weeks, validate_hours, WEEKS_MAP, HOURS_MAP
from .bases import profile, write_to_name_category, read_from_category, delete_category, write_to_set_category, \
    write_to_definitions, read_from_definitions, delete_definition


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
    data_add_definition = None
    data_add_category = None
    data_set = None
    selected_category = None
    selected_definition = None
    name_definition = None
    question_definition = None
    set_category = None
    button_back = '<Назад>'
    button_yes = '<Да>'
    button_no = '<Нет>'
    button_del = '<Удалить>'
    definition = '<Определения>'
    button_settings = '<Настройка>'
    buttons_into_category = [
        definition,
        button_settings,
        button_del,
        button_back
    ]
    buttons_into_definition = [
        button_del,
        button_back,
    ]
    buttons_yes_no = [
        button_no,
        button_yes,
    ]

    @log_errors
    def do_start(self, update, context):
        p, _ = profile(update, update.message.chat_id)
        reply_markup = get_buttons_cd(read_from_category(p))
        if not _:
            self.selected_category = None
            text = '__ВКЛЮЧЕНИЕ__\n\nС Возвращением!\nВыберите Категорию:'
            update.message.reply_text(text=text, reply_markup=reply_markup)
        else:
            self.selected_category = None
            text = '__ВКЛЮЧЕНИЕ__\n\nДобро пожаловать!\nВыберите Категорию знаний, которые вы будите закреплять\n\n'
            update.message.reply_text(text=text, reply_markup=reply_markup)

    @log_errors
    def do_print(self, update, context):
        print('do_print')
        p, _ = profile(update, update.message.chat_id)

        if not self.selected_category and self.data_add_category == '__<ADD>__':
            # Press button <Добавить>
            write_to_name_category(p, update.message.text)
            reply_markup = get_buttons_cd(read_from_category(p))
            self.data_add_category = None
            self.selected_category = None
            text = f"""__МЕНЮ КАТЕГОРИЙ__                                                                             .
\n\nДобавлена Категория "{update.message.text}"
\n\nВыберите Категорию"""
            update.message.reply_text(text=text, reply_markup=reply_markup)

        elif self.selected_category and self.set_category and self.data_set == self.button_settings:
            # Press button Category -> Настройка -> Настройка недели
            self.set_hours(update, context)

        elif self.selected_category and self.data_set == self.button_settings:
            # Press button Category -> Настройка
            self.set_weeks(update, context)

        elif self.selected_category and self.data_add_definition == '__<ADD>__':
            # Press a category -> definition -> button <Добавить>

            self.name_definition = update.message.text
            text = f"""__ДОБАВЛЕНИЕ ОПРЕДЕЛЕНИЯ В КАТЕГОРИИ "{self.selected_category}"__                               .
\n\nДобавлено определение "{update.message.text}"
\n\nТеперь введите вопрос к определению, вы будете получать его в рамках опроса."""
            update.message.reply_text(text=text)
            self.data_add_definition = '__<ADD_ASK>__'

        elif self.selected_category and self.data_add_definition == '__<ADD_ASK>__':
            # Write the name_definition

            self.question_definition = update.message.text
            text = f"""__ДОБАВЛЕНИЕ ОПРЕДЕЛЕНИЯ В КАТЕГОРИИ "{self.selected_category}"__                               .
\n\nДобавлен вопрос:\n"{update.message.text}"
\n\nТеперь введите текст самого определения"""
            update.message.reply_text(text=text)
            self.data_add_definition = '__<ADD_TEXT>__'

        elif self.selected_category and self.data_add_definition == '__<ADD_TEXT>__':
            # Write the name_definition

            write_to_definitions(p, self.selected_category, update.message.text,
                                 self.name_definition, self.question_definition)
            text = f"""__ДОБАВЛЕНИЕ ОПРЕДЕЛЕНИЯ В КАТЕГОРИИ "{self.selected_category}"__                               .
\n\nДобавлено определение:\n"{self.name_definition}"
\nВопрос: {self.question_definition}\nТекст: {update.message.text}"""
            self.data_add_definition = None
            self.name_definition = None
            self.question_definition = None
            list_for_buttons = [i for i in read_from_definitions(p, self.selected_category)]
            list_for_buttons.append(self.button_back)
            reply_markup = get_buttons_cd(list_for_buttons)
            update.message.reply_text(text=text, reply_markup=reply_markup)

        else:
            text = f'update.message.text = {update.message.text}\n\nself.data_set = {self.data_set}'
            update.message.reply_text(text)

    @log_errors
    def button_inline(self, update: Update, context):
        print('button_inline')
        query = update.callback_query
        query.answer()
        p, _ = profile(update, update.effective_message.chat_id)

        if not self.selected_category and query.data == '__<ADD>__':
            # Press button Add
            # TODO: Filter the same categories

            self.data_add_category = query.data
            text = """__ДОБАВЛЕНИЕ КАТЕГОРИИ__\n\nВведите название новой Категории:"""
            query.edit_message_text(text=text)

        elif query.data in [str(i) for i in read_from_category(p)] and query.data != '__<ADD>__':
            # Press a Category

            self.selected_category = query.data
            text = f"""__ВНУТРИ КАТЕГОРИИ "{self.selected_category}"__                                                 .                                                                              
\n\nВыбрана Категория "{self.selected_category}"
\n\nВыберите кнопки:"""
            query.edit_message_text(text=text, reply_markup=get_keyboard_into(self.buttons_into_category))

        elif not self.selected_definition and self.selected_category and query.data == self.button_del:
            # Press button Category -> Удалить

            text = f'__УДАЛЕНИЕ КАТЕГОРИИ__\n\nВы уверены что хотите удалить категорию "{self.selected_category}"?'
            query.edit_message_text(text=text, reply_markup=get_keyboard_into(self.buttons_yes_no))

        elif not self.selected_definition and self.selected_category and query.data == self.button_no:
            # Press button Category -> Удалить -> Нет

            text = f"""__ВНУТРИ КАТЕГОРИИ__                                                                           .
\n\nВыбрана Категория "{self.selected_category}"
\n\nВыберите кнопки:"""
            query.edit_message_text(text=text, reply_markup=get_keyboard_into(self.buttons_into_category))

        elif not self.selected_definition and self.selected_category and query.data == self.button_yes:
            # Press button Category -> Удалить -> Да

            delete_category(p, self.selected_category)
            self.selected_category = None
            text = """__МЕНЮ КАТЕГОРИЙ__                                                                             .
            \n\nКатегория удалена.\n\n
            Выберите Категорию:"""
            reply_markup = get_buttons_cd(read_from_category(p))
            query.edit_message_text(text=text, reply_markup=reply_markup)

        elif not self.selected_definition and self.selected_category and query.data == self.button_back:     #
            # Press button Category -> Назад
            reply_markup = get_buttons_cd(read_from_category(p))
            self.selected_category = None
            text = """
            __МЕНЮ КАТЕГОРИЙ__                                                                                       .
            \n\nВыберите Категорию:'
            """
            query.edit_message_text(text=text, reply_markup=reply_markup)

        elif self.selected_category and query.data == self.button_settings:
            # Press button Category -> Настройка

            self.data_set = query.data
            weeks_map = [f"{key} - {value}" for key, value in WEEKS_MAP.items()]
            weeks_map = "\n".join(weeks_map)
            text = f"""__НАСТРОЙКА КАТЕГОРИИ__
\n\nВыберите дни недели из списка:\n
Сообщения с определениями будут отправляться с 08:00 до 22:00 с понедельника по пятницу.'
\n\n{weeks_map}"""
            query.edit_message_text(text=text)
            self.set_category = None

        elif self.selected_category and query.data == self.definition:     #
            # Press button Category -> Определения

            list_for_buttons = [i for i in read_from_definitions(p, self.selected_category)]
            list_for_buttons.append(self.button_back)
            reply_markup = get_buttons_cd(list_for_buttons)
            text = """
            __МЕНЮ ОПРЕДЕЛЕНИЙ__                                                                                     .
            \n\nВыберите определение:
            """
            query.edit_message_text(text=text, reply_markup=reply_markup)

        elif not self.selected_definition and self.selected_category and query.data == self.button_back:
            # Press a Category -> Определения -> Назад

            text = f"""__ВНУТРИ КАТЕГОРИИ__                                                                           .
\n\nВыберете кнопки:"""
            query.edit_message_text(text=text, reply_markup=get_keyboard_into(self.buttons_into_category))

        elif query.data in [str(i) for i in read_from_definitions(p, self.selected_category)] \
                and query.data != '__<ADD>__':
            # Press button Category -> Определения -> Press a definition
            # TODO: Filter the same definitions

            self.selected_definition = query.data
            text = f"""__ВНУТРИ ОПРЕДЕЛЕНИЯ__                                                                          .
\n\nВыбрано определение "{self.selected_definition}"
\n\nВыберите кнопки:"""
            query.edit_message_text(text=text, reply_markup=get_keyboard_into(self.buttons_into_definition))

        elif self.selected_category and query.data == '__<ADD>__':
            # Press button Category -> Определения -> Press a definition -> button Add

            self.data_add_definition = query.data
            text = """__ДОБАВЛЕНИЕ ОПРЕДЕЛЕНИЯ__
            \n\nВведите название нового определения:"""
            query.edit_message_text(text=text)

        elif self.selected_definition and query.data == self.button_back:     # self.selected_category and
            # Press button Category -> Определения -> Press a definition -> Назад

            list_for_buttons = [i for i in read_from_definitions(p, self.selected_category)]
            list_for_buttons.append(self.button_back)
            reply_markup = get_buttons_cd(list_for_buttons)
            self.selected_definition = None
            text = """
            __МЕНЮ ОПРЕДЕЛЕНИЙИЙ__
            \n\nВыберите определение:
            """
            query.edit_message_text(text=text, reply_markup=reply_markup)

        elif self.selected_definition and query.data == self.button_del:
            # Press button Category -> Определения -> Press a definition -> Удалить

            text = f"""__УДАЛЕНИЕ ОПРЕДЕЛЕНИЯ__
\n\nВы уверены что хотите удалить определение "{self.selected_definition}"?"""
            query.edit_message_text(text=text, reply_markup=get_keyboard_into(self.buttons_yes_no))

        elif self.selected_definition and query.data == self.button_no:
            # Press button Category -> Удалить -> Нет

            text = f"""__ВНУТРИ ОПРЕДЕЛЕНИЯ__                                                                       .
\n\nВыбрано определение "{self.selected_definition}"
\n\nВыберите кнопки:"""
            query.edit_message_text(text=text, reply_markup=get_keyboard_into(self.buttons_into_definition))

        elif self.selected_definition and query.data == self.button_yes:
            # Press button Category -> Удалить -> Да

            delete_definition(p, self.selected_definition)
            self.selected_definition = None
            text = """__МЕНЮ ОПРЕДЕЛЕНИЙ__                                                                          .
            \n\nОпределение удалено.\n\nВыберите определение:"""
            list_for_buttons = [i for i in read_from_definitions(p, self.selected_category)]
            list_for_buttons.append(self.button_back)
            reply_markup = get_buttons_cd(list_for_buttons)
            query.edit_message_text(text=text, reply_markup=reply_markup)

        else:
            reply_markup = get_buttons_cd(read_from_category(p))
            text = f'Что-то пошло не так\n\nself.selected_category = ' \
                   f'{self.selected_category}\n\nquery.data = {query.data}'
            query.edit_message_text(text=text, reply_markup=reply_markup)

    @log_errors
    def cancel(self, update, context):
        # user = update.message.from_user
        # logger.info("User %s canceled the conversation.", user.first_name)
        update.message.reply_text('Bye! I hope we can talk again some day.')  # reply_markup=ReplyKeyboardRemove())

    @log_errors
    def set_weeks(self, update, context):
        print('set_weeks', self.data_set)

        # get weeks
        weeks = validate_weeks(text=update.message.text)
        if weeks is None:
            text = """
            __НАСТРОЙКА КАТЕГОРИИ__
            \n\nПожалуйста, укажите корректный период!
            """
            update.message.reply_text(text=text)
            # self.do_print(update, context)
            return

        # ask about hours
        hours_map = [f"{key} - {value}" for key, value in HOURS_MAP.items()]
        hours_map = "\n".join(hours_map)
        text = f"""
        __НАСТРОЙКА КАТЕГОРИИ__
\n\nСколько раз за день вы хотите получать сообщения?
\nВыберите из списка:\n{hours_map}'
        """
        update.message.reply_text(text=text)
        self.set_category = str(weeks)

    @log_errors
    def set_hours(self, update, context):
        print('set_hours', self.data_set)

        # get weeks
        hours = validate_hours(text=update.message.text)
        if hours is None:
            text = """
            __НАСТРОЙКА КАТЕГОРИИ__
            \n\nПожалуйста, укажите корректный часовой период!
            """
            update.message.reply_text(text=text)
            # return self.do_print(update, context)
            return
        p, _ = profile(update, update.message.chat_id)

        # ask about hours
        text = """__ВНУТРИ КАТЕГОРИИ__                                                                              .
        \n\nНастройки сохранены\nВыберете кнопки"""
        reply_markup = get_keyboard_into(self.buttons_into_category)
        update.message.reply_text(text=text, reply_markup=reply_markup)
        self.set_category = self.set_category + ', ' + str(hours)
        write_to_set_category(p, self.selected_category, self.set_category)

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
