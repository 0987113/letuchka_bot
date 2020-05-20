#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
from django.core.management.base import BaseCommand
from django.conf import settings
from telegram import Update
from telegram.ext import Updater, CommandHandler, Filters, MessageHandler, CallbackQueryHandler
from .keyboards import *
from .bases import *
from .buttons_handler import *

# TODO: прикрутить кнопку домой
# TODO: удалать вссе неактуальные сообщения бота
# TODO: PostgreSQL
# TODO: заменить все if else на словари


def log_errors(f):
    # TODO: сделать полноценный обработчик исключений и варианты действия в этих случая:
    #  ошибка базы, сервер молчит

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
    tasks = []

    help = 'Телеграм-бот'
    data_add_definition = None
    data_add_category = None
    set_safety = None
    selected_category = None
    selected_definition = None
    name_definition = None
    question_definition = None
    set_category = None
    safety_button_back = None

    @log_errors
    def do_start(self, update, context):
        p, _ = profile(update, update.message.chat_id)
        reply_markup = get_buttons(read_from_category(p), 'add')
        write_to_profile_start(p, 'working')   # начинаем работу алгоритма опросов
        self.safety_button_back = None
        self.selected_category = None   # сбрасываем нахождение в into_category
        if not _:
            update.message.reply_text(text=text_hello, reply_markup=reply_markup)
        else:
            update.message.reply_text(text=text_welcome, reply_markup=reply_markup)

    @log_errors
    def do_stop(self, update, context):
        p, _ = profile(update, update.message.chat_id)
        reply_markup = get_buttons(read_from_category(p), 'add')
        write_to_profile_start(p, 'stopped')  # начинаем работу алгоритма опросов
        self.safety_button_back = None
        self.selected_category = None  # сбрасываем нахождение в into_category
        if not _:
            update.message.reply_text(text=text_bye, reply_markup=reply_markup)
        else:
            print('КОМАНДА СТОП, А ПРОФИЛЬ НЕ В БАЗЕ')

    @log_errors
    def do_print(self, update, context):
        # TODO: проверка входящих данных для имени кнопки
        p, _ = profile(update, update.message.chat_id)
        print('do_print')

        # есть категория
        if self.selected_category:

            # есть определение
            if self.data_add_definition:

                # press a category -> definitions -> button <добавить> или <создать>
                if self.data_add_definition in [Buttons.button_add, Buttons.button_create]:
                    if update.message.text in [str(i) for i in read_from_definitions(p, self.selected_category)]:
                        update.message.reply_text(text=text_add_definition_error(self.selected_category))
                    else:
                        self.name_definition = update.message.text
                        update.message.reply_text(
                            text=text_add_definition_one(self.name_definition, self.selected_category))
                        self.data_add_definition = '__<ADD_ASK>__'

                # write the name_definition
                elif self.data_add_definition == '__<ADD_ASK>__':
                    self.question_definition = update.message.text
                    update.message.reply_text(
                        text=text_add_definition_two(self.question_definition, self.selected_category))
                    self.data_add_definition = '__<ADD_TEXT>__'

                # write_to_definitions
                elif self.data_add_definition == '__<ADD_TEXT>__':
                    write_to_definitions(
                        p,
                        self.selected_category,
                        update.message.text,
                        self.name_definition,
                        self.question_definition)   # после этой операции бот завис
                    reply_markup = get_buttons(read_from_definitions(p, self.selected_category), 'two')
                    update.message.reply_text(
                        text=text_add_definition_three(self.name_definition, self.selected_category),
                        reply_markup=reply_markup)
                    self.data_add_definition = None
                    self.name_definition = None
                    self.question_definition = None
                    self.safety_button_back = 'from_menu_definition_to_into_category'  # чтобы вернуться в категорию

            # Работаем с настройками категории
            elif self.set_safety:
                print('self.set_safety = ', self.set_safety, 'self.set_category = ', self.set_category)

                if self.set_category and self.set_safety == Buttons.button_settings:
                    # Press button Category -> Настройка -> Настройка недели
                    self.set_hours(update)

                # Press button Category -> Настройка (после введеного значения мы проверяем наличие переменной)
                elif self.set_safety == Buttons.button_settings:
                    self.set_weeks(update)

        elif not self.selected_category:

            # Press button <Добавить> или <Создать> (category)
            if self.data_add_category in [Buttons.button_add, Buttons.button_create]:

                if update.message.text in [str(i) for i in read_from_category(p)]:
                    update.message.reply_text(text=text_text_add_category_error)
                else:
                    write_to_name_category(p, update.message.text)
                    reply_markup = get_buttons(read_from_category(p), 'add')
                    self.data_add_category = None
                    self.selected_category = None
                    self.safety_button_back = None  # сбрасываем нахождение в into_category
                    update.message.reply_text(text=text_show_category, reply_markup=reply_markup)

        else:
            text = f'update.message.text = {update.message.text}'
            update.message.reply_text(text)

    @log_errors
    def button_inline(self, update: Update, context):
        print('button_inline')
        query = update.callback_query
        query.answer()
        p, _ = profile(update, update.effective_message.chat_id)

        # категория выбрана
        if self.selected_category:
            print('категория выбрана')

            # определение выбрано
            if self.selected_definition:
                print('определение выбрано')

                if query.data == Buttons.button_del:
                    # Press button Category -> Определения -> Press a definition -> Удалить
                    query.edit_message_text(
                        text=text_del_definition_ask(self.selected_category, self.selected_definition),
                        reply_markup=get_buttons(Buttons.buttons_yes_no, 'None'))

                elif query.data == Buttons.button_no:
                    # Press button Category -> Определения -> Press a definition -> Удалить -> Нет
                    data_definition, question = read_from_definitions_data(p, self.selected_category,
                                                                           self.selected_definition)
                    query.edit_message_text(
                        text=text_into_definition(
                            self.selected_category,
                            self.selected_definition,
                            question,
                            data_definition),
                        reply_markup=get_buttons(Buttons.buttons_into_definition, 'back'))
                    self.safety_button_back = 'into_definition'     # внутри определения

                # press button category -> определния -> выбрано определение -> удалить -> Да
                elif query.data == Buttons.button_yes:
                    delete_definition(p, self.selected_definition)
                    reply_markup = get_buttons(read_from_definitions(p, self.selected_category), 'two')
                    query.edit_message_text(
                        text=text_del_definition_ready(self.selected_category, self.selected_definition),
                        reply_markup=reply_markup,
                    )
                    self.selected_definition = None
                    self.safety_button_back = 'from_menu_definition_to_into_category'  # чтобы вернуться в категорию

                # возвращаемся из press button category -> определения -> press a definition в меню определений
                elif self.safety_button_back == 'into_definition':

                    # press button category -> определения -> press a definition -> назад
                    if query.data == Buttons.button_back:
                        self.selected_definition = None
                        self.safety_button_back = 'from_menu_definition_to_into_category'  # чтобы вернуться в категорию
                        query.edit_message_text(
                            text=text_show_definitions(self.selected_category),
                            reply_markup=get_buttons(read_from_definitions(p, self.selected_category), 'two'))

            # определение не выбрано
            elif not self.selected_definition:
                print('определение не выбрано')

                # press button category -> удалить
                if query.data == Buttons.button_del:
                    print('1')
                    query.edit_message_text(
                        text=text_del_category_ask(self.selected_category),
                        reply_markup=get_buttons(Buttons.buttons_yes_no, 'None'))

                # Press button Category -> Удалить -> Нет
                elif query.data == Buttons.button_no:
                    print('2')
                    set_questions = read_from_category_set(p, self.selected_category, 'text_result')
                    query.edit_message_text(
                        text=text_into_category(self.selected_category, set_questions),
                        reply_markup=get_buttons(Buttons.buttons_into_category, 'add'))
                    self.safety_button_back = 'into_category'  # мы внутри категории

                # Press button Category -> Определения
                elif query.data == Buttons.definitions:
                    print('3_Press button Category -> Определения')
                    reply_markup = get_buttons(read_from_definitions(p, self.selected_category), 'two')
                    text = text_show_definitions(self.selected_category)
                    query.edit_message_text(text=text,
                                            reply_markup=reply_markup)
                    self.safety_button_back = 'from_menu_definition_to_into_category'  # чтобы вернуться в категорию
                    print('safety_button_back', self.safety_button_back)

                # Press button Category -> Удалить -> Да
                elif query.data == Buttons.button_yes:
                    print('4')
                    delete_category(p, self.selected_category)
                    reply_markup = get_buttons(read_from_category(p), 'add')
                    query.edit_message_text(
                        text=text_del_category_ready(self.selected_category),
                        reply_markup=reply_markup)
                    self.selected_category = None
                    self.safety_button_back = None  # сбрасываем нахождение в into_category

                # press button category -> настройка
                elif query.data == Buttons.button_settings:
                    print('6_Настройка')
                    self.set_safety = query.data  # Записываем переменную для пропуска в следующую функцию
                    weeks_map = [f"{key} - {value}" for key, value in WEEKS_MAP.items()]
                    weeks_map = "\n".join(weeks_map)
                    query.edit_message_text(text=text_set_category(weeks_map, self.selected_category))

                # Press button Category -> Определения -> button Add
                elif query.data in [Buttons.button_add, Buttons.button_create]:
                    print('7_Press button Category -> Определения -> button Add')
                    self.data_add_definition = query.data
                    query.edit_message_text(text=text_add_definition(self.selected_category))

                # Press button Category -> Определения -> Press a definition
                elif query.data in [str(i) for i in read_from_definitions(p, self.selected_category)]:
                    print('8')
                    self.selected_definition = query.data
                    data_definition, question = read_from_definitions_data(
                        p,
                        self.selected_category,
                        self.selected_definition)
                    query.edit_message_text(
                        text=text_into_definition(
                            self.selected_category,
                            self.selected_definition,
                            question,
                            data_definition),
                        reply_markup=get_buttons(Buttons.buttons_into_definition, 'back'))
                    self.safety_button_back = 'into_definition'     # внутри определения

                # выходим из category -> определения в into_category
                elif self.safety_button_back == 'from_menu_definition_to_into_category':
                    print('выходим из category -> определения в into_category')

                    # press a category -> определения -> назад
                    if query.data == Buttons.button_back:
                        set_questions = read_from_category_set(p, self.selected_category, 'text_result')
                        query.edit_message_text(
                            text=text_into_category(self.selected_category, set_questions),
                            reply_markup=get_buttons(Buttons.buttons_into_category, 'back'))
                        self.safety_button_back = 'into_category'  # мы внутри категории

                # выходим из category в меню категорий
                elif self.safety_button_back == 'into_category':
                    print('9')

                    # меню категорий -> press button Category -> Назад
                    if query.data == Buttons.button_back:
                        reply_markup = get_buttons(read_from_category(p), 'add')
                        self.selected_category = None

                        query.edit_message_text(
                            text=text_show_category,
                            reply_markup=reply_markup)
                        self.safety_button_back = None  # сбрасываем нахождение в into_category

                else:
                    print('НИЧЕГО НЕ ВЫБРАНО, query.data = ', query.data)

        # категория не выбрана
        elif not self.selected_category:
            print('категория не выбрана')

            # меню категорий -> press button add or create
            if query.data in [Buttons.button_add, Buttons.button_create]:
                print('меню категорий -> press button add or create')
                self.data_add_category = query.data
                query.edit_message_text(text=text_add_category)

            # меню категорий -> press a category
            elif query.data in [str(i) for i in read_from_category(p)]:
                print('меню категорий -> press a category')
                self.selected_category = query.data
                set_questions = read_from_category_set(p, self.selected_category, 'text_result')
                query.edit_message_text(
                    text=text_into_category(self.selected_category, set_questions),
                    reply_markup=get_buttons(Buttons.buttons_into_category, 'back'))
                self.safety_button_back = 'into_category'  # мы внутри категории

        else:
            reply_markup = get_buttons(read_from_category(p), 'add')
            text = f'Что-то пошло не так\n\nself.selected_category = ' \
                   f'{self.selected_category}\n\nquery.data = {query.data}'
            query.edit_message_text(text=text, reply_markup=reply_markup)
            self.safety_button_back = None  # сбрасываем нахождение в into_category

    @log_errors
    def set_weeks(self, update):
        weeks = validate_weeks(text=update.message.text)
        hours_map = [f"{key} - {value}" for key, value in HOURS_MAP.items()]
        hours_map = "\n".join(hours_map)
        if weeks is None:
            weeks_map = [f"{key} - {value}" for key, value in WEEKS_MAP.items()]
            weeks_map = "\n".join(weeks_map)
            update.message.reply_text(
                text=text_set_weeks(self.selected_category, 'None', hours_map, weeks_map))
            return
        # ask about hours
        update.message.reply_text(
            text=text_set_weeks(self.selected_category, 'ok', hours_map, 'None'))
        self.set_category = str(weeks)

    @log_errors
    def set_hours(self, update):
        print('set_hours')
        # get hours
        hours = validate_hours(text=update.message.text)
        if hours is None:
            hours_map = [f"{key} - {value}" for key, value in HOURS_MAP.items()]
            hours_map = "\n".join(hours_map)
            update.message.reply_text(text=text_set_hours(self.selected_category, 'None', 'None', hours_map))
            return
        p, _ = profile(update, update.message.chat_id)
        self.set_category = self.set_category + ', ' + str(hours)
        write_to_set_category(p, self.selected_category, self.set_category)
        # ask about hours
        reply_markup = get_buttons(Buttons.buttons_into_category, 'back')
        set_questions = read_from_category_set(p, self.selected_category, 'text_result')
        print('set_questions =', set_questions)
        update.message.reply_text(
            text=text_set_hours(self.selected_category, 'ok', set_questions, 'None'),
            reply_markup=reply_markup)
        self.set_category = None  # обнуляем для повторного использования
        self.set_safety = None  # обнуляем для защиты запуска
        self.safety_button_back = 'into_category'  # мы внутри категории

    @log_errors
    def handle(self, *args, **options):
        updater = Updater(token=settings.TG_TOKEN, base_url=settings.TG_PROXY_URL, use_context=True)
        updater.dispatcher.add_handler(CommandHandler('start', self.do_start))
        updater.dispatcher.add_handler(CommandHandler('stop', self.do_stop))
        updater.dispatcher.add_handler(MessageHandler(Filters.text, self.do_print))
        updater.dispatcher.add_handler(CallbackQueryHandler(self.button_inline))

        updater.start_polling()
        updater.idle()


if __name__ == '__main__':
    с = Command()
    с
