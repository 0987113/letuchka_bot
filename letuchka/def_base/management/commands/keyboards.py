from telegram import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup


class Buttons:
    button_create = '<Создать>'
    button_add = '<Добавить>'
    button_back = '<Назад>'
    button_yes = '<Да>'
    button_no = '<Нет>'
    button_del = '<Удалить>'
    definitions = '<Определения>'
    button_settings = '<Настройка>'
    change = '<Изменить>'
    buttons_into_category = [
        definitions,
        button_settings,
        button_del,
    ]
    buttons_into_definition = [
        change,
        button_del,
    ]
    buttons_yes_no = [
        button_no,
        button_yes,
    ]


# TODO: correct fonts

# ________________________________________________________________
text_add_category = """
Добавление новой категории.

Мы советуем называть категорию по ролевантности данных, которые будут храниться в ней. Например "Английский".

Отправьте нам ее название:"""

# ________________________________________________________________
text_text_add_category_error = """
Добавление новой категории.

Вы ввели название уже имеющейся категории. Введите пожалуйста название новой Категории: """

# ________________________________________________________________
text_hello = """
Бот запущен.

С Возвращением! Если у Вас есть заполненные категории они сразу начнут работать.

Выберете категорию из представленных ниже, для настройки периодичности опросов, удаления или добавления определений.\
"""

# ________________________________________________________________
text_bye = """
Бот остановлен.

Вы можете работать с категориями, но опрос производиться не будет.

Выберете категорию из представленных ниже, для настройки периодичности опросов, удаления или добавления определений.\
"""

# ________________________________________________________________
text_welcome = """
Добро пожаловать в наш проект "Летучка". 

Этот Бот поможет Вам запомнить любую информацию, какую Вы только захотите!

Чтобы приступить к изучению информации, создайте кетегорию данных, с которыми будете работать. Добавьте туда данные\
 и Бот будет в указанное вами время просить Вас вспомнить эти данные."""

# ________________________________________________________________
text_show_category = """
Меню категорий.

Выберете категорию из представленных ниже, для настройки периодичности опросов, удаления или добавления определений."""


# ________________________________________________________________
def len_buttons(buttons: list, command):
    add_button = InlineKeyboardButton(f'{Buttons.button_add}', callback_data=f'{Buttons.button_add}')
    create_button = InlineKeyboardButton(f'{Buttons.button_create}', callback_data=f'{Buttons.button_create}')
    back_button = InlineKeyboardButton(f'{Buttons.button_back}', callback_data=f'{Buttons.button_back}')
    keyboard_into = []

    if len(buttons) == 1 and command != 'two':
        if command == 'add' and len(buttons) > 0:
            return add_button
        elif command == 'add' and len(buttons) == 0:
            return create_button
        elif command == 'back':
            return back_button
    elif len(buttons) > 2 and len(buttons) % 2 != 0 and command != 'two':
        if command == 'add' and len(buttons) > 0:
            return add_button
        elif command == 'add' and len(buttons) == 0:
            return create_button
        elif command == 'back':
            return back_button
    elif command == 'add' and len(buttons) > 0:
        keyboard_into.append(add_button)
    elif command == 'add' and len(buttons) == 0:
        keyboard_into.append(create_button)
    elif command == 'two' and len(buttons) > 0:
        keyboard_into.append(add_button)
        keyboard_into.append(back_button)
    elif 2 > len(buttons) >= 0 and command == 'two':
        keyboard_into.append(create_button)
        keyboard_into.append(back_button)
    elif command == 'back':
        keyboard_into.append(back_button)
    elif command == 'None':
        return keyboard_into
    return keyboard_into


# ________________________________________________________________
def get_buttons(buttons: list, command):
    """
    :param buttons:
    :param command:  Button back, create and add:
    If 'add' - add,
    elif 'two' - add and back,
    elif 'back' - only back.
    elif 'None' is nothing.
    :return:
    """
    print('get_buttons', len(buttons), 'command=', command)
    keyboard = []

    if 0 < len(buttons) <= 2:
        keyboard_into = []
        for i in range(len(buttons)):
            button = InlineKeyboardButton(f'{buttons[i]}', callback_data=f'{buttons[i]}')
            if len(buttons) == 1 and command != 'two':
                keyboard_into.append(button)
                # Если первая кнопка в ряду готова
                last_button = len_buttons(buttons, command)
                keyboard_into.append(last_button)
                keyboard.append(keyboard_into)
            # Две кнопки
            else:
                keyboard_into.append(button)
                # если первый ряд заполнен или кнопка одна но мы добавляем две
                if i == 1 or len(buttons) == 1:
                    keyboard.append(keyboard_into)
                    last_keyboards = len_buttons(buttons, command)
                    keyboard.append(last_keyboards)
    elif 8 >= len(buttons) > 2:
        # TODO: Button NEXT
        total_count = 0
        penultimate_button = len(buttons) - 1
        try_pair = len(buttons) % 2
        while len(buttons) > total_count:
            count = 0
            keyboard_into = []
            while count < 2 and total_count < len(buttons):
                button = InlineKeyboardButton(f'{buttons[total_count]}', callback_data=f'{buttons[total_count]}')
                # Если не последний ряд просто аполняем его
                if total_count != penultimate_button:
                    keyboard_into.append(button)
                    count += 1
                    total_count += 1
                # Если последний ряд с одной кнопкой добавляем нашу ОДНУ кнопку
                elif command in ['add', 'back'] and total_count == penultimate_button and try_pair == 1:
                    # сохраняем последнюю кнопку
                    keyboard_into.append(button)

                    # запрашиваем наши кнопки
                    last_keyboards = len_buttons(buttons, command)

                    # сохраняем нашу кнопку в строке
                    keyboard_into.append(last_keyboards)

                    count += 1
                    total_count += 1

                # Если последний ряд с двумя кнопкми или две наши кнопки добавляем последнюю кнопку из словаря
                elif command == 'two' or try_pair != 1:

                    # сохраняем последнюю кнопку
                    keyboard_into.append(button)

                    count += 1
                    total_count += 1

            keyboard.append(keyboard_into)

        # Если последний ряд с двумя кнопками или две наши кнопки добавляем в новую строку нашу кнопку
        if try_pair == 0 or command == 'two':

            last_keyboards = len_buttons(buttons, command)
            keyboard.append(last_keyboards)
    # Если кнопок больше восьми, их надо делить на пакеты
        """elif len(buttons) > 8:
        keyboard = next(generator_next_buttons(buttons, command))"""
    elif len(buttons) == 0:
        last_keyboards = len_buttons(buttons, command)
        keyboard.append(last_keyboards)
    return InlineKeyboardMarkup(keyboard)


def generator_next_buttons(buttons, command):
    keyboard = []
    max_count = 8
    total_count = 0
    penultimate_button = len(buttons) - 1
    try_pair = len(buttons) % 2
    # предлага передать этот процесс генераторной функции
    while len(buttons) > total_count:
        # пока счет не дойдет до восьми, т е выполняем стандартное заполнение
        while max_count > total_count:
            count = 0
            keyboard_into = []
            # упаковываем по 2 в ряд
            while count < 2 and total_count < len(buttons):
                button = InlineKeyboardButton(f'{buttons[total_count]}', callback_data=f'{buttons[total_count]}')
                # Если не последний ряд просто аполняем его
                if total_count != penultimate_button:
                    keyboard_into.append(button)
                    count += 1
                    total_count += 1
                # Если последний ряд с одной кнопкой добавляем нашу ОДНУ кнопку
                elif command in ['add', 'back'] and total_count == penultimate_button and try_pair == 1:
                    # сохраняем последнюю кнопку
                    keyboard_into.append(button)
                    # запрашиваем наши кнопки
                    last_keyboards = len_buttons(buttons, command)
                    # сохраняем нашу кнопку в строке
                    keyboard_into.append(last_keyboards)
                    count += 1
                    total_count += 1
                # Если последний ряд с двумя кнопкми или две наши кнопки добавляем последнюю кнопку из словаря
                elif command == 'two' or try_pair != 1:
                    # сохраняем последнюю кнопку
                    keyboard_into.append(button)
                    count += 1
                    total_count += 1
            keyboard.append(keyboard_into)
    # Если последний ряд с двумя кнопками или две наши кнопки добавляем в новую строку нашу кнопку
    if try_pair == 0 or command == 'two':
        last_keyboards = len_buttons(buttons, command)
        keyboard.append(last_keyboards)
    return keyboard


# ________________________________________________________________
def text_del_category_ask(category):
    output_text = f"""
Удаление категории "{category}"


Вы уверены что хотите удалить категорию и все ее определения? Отменить это действие будет невозможно."""
    return output_text


# ________________________________________________________________
def text_del_category_ready(category):
    output_text = f"""
Категория "{category}" удалена.

Выберете категорию из представленных ниже, для настройки периодичности опросов или удаления или добавления определений.\
"""
    return output_text


# ________________________________________________________________
def text_into_category(category, set_questions):
    output_category = f"""
Категория "{category}"
Периодичность опросов: {set_questions}

Вы можете перейти к определениям, удалить категорию и все ее определения или настроить периодичность отправки Вам\
 опросов."""
    return output_category


# ________________________________________________________________
def text_add_definition_error(category):
    output = f"""
Категория "{category}"
Добавление нового определения.

Вы ввели название уже имеющегося определения. Введите пожалуйста название нового определения:"""
    return output


# ________________________________________________________________
def text_add_definition_one(input_text, category):
    output_definition = f"""
Категория "{category}"

Бот сохранил "{input_text}", введите пожалуйста вопрос к определению, Вы будете получать его в рамках опроса.\
 Например "Что такое Present Simple?"."""
    return output_definition


# ________________________________________________________________
def text_add_definition_two(input_text, category):
    output_definition = f"""
Категория "{category}"

Бот сохранил вопрос:
"{input_text}"

Ведите пожалуйста сам текст определения, после ответа на вопрос, Вы сможете посмотреть его и сравнить с ответом.\
 Например:
"Это простое настоящее время, обозначающее действие в самом широком смысле этого слова"."""
    return output_definition


# ________________________________________________________________
def text_add_definition_three(input_text, category):
    output_definition = f"""
Категория "{category}"

Бот сохранил определение "{input_text}". Выбрав его Вы сможете его просмотреть, изменить или удалить. """
    return output_definition


# ________________________________________________________________
def text_show_definitions(category):
    output_definitions = f"""
Категория "{category}"
Меню определений.

Вы можете добавить новое определение или выбрать из представленных ниже, для его просмотра, изменения или удаления."""
    return output_definitions


# ________________________________________________________________
def text_into_definition(category, definition, question, data):
    output = f"""
Категория "{category}"
Определение "{definition}"

Вопрос к определению: 
"{question}"

Текст этого определения:
"{data}"

Так же Вы можете удалить или изменить данное определение."""
    return output


# ________________________________________________________________
def text_add_definition(category):
    output = f"""
Категория "{category}"
Добавление нового определения.

Мы советуем называть определение по его обобщенному содержимому, которое будет храниться в нем. Например \
"Present Simple".

Отправьте нам его название:"""
    return output


# ________________________________________________________________
def text_del_definition_ask(category, definition):
    output = f"""
Категория "{category}"

Вы уверены что хотите удалить определение "{definition}"? Отменить это действие будет невозможно."""
    return output


# ________________________________________________________________
def text_del_definition_ready(category, definition):
    output = f"""
Категория "{category}"

Определение "{definition}" удалено.

Вы можете добавить новое или выбрать определение из представленных ниже, для его просмотра, изменения или удаления."""
    return output


# ________________________________________________________________
def text_set_category(w_map, category):
    output_set = f"""
Категория "{category}"

Для того чтобы настроить периодичность опросов в данной категории, выберите пожалуйста подходящий вариант из списка:

{w_map}"""
    return output_set


# ________________________________________________________________
def text_set_weeks(category, command, hours_map='', w_map=''):
    if command == 'ok':
        output = f"""
Категория "{category}"

Для того чтобы настроить периодичность опросов в течении дня, пожалуйста, выберите пожалуйста подходящий вариант\
 из списка:

{hours_map}"""
    else:
        output = f"""
Категория "{category}"

Пожалуйста, укажите корректный период, выбите подходящий вариант из списка:

{w_map}"""
    return output


# ________________________________________________________________
def text_set_hours(category, command, set_questions, hours_map=''):
    if command == 'ok':
        output = f"""
Категория "{category}"
Периодичность опросов: {set_questions}

Бот сохранил настройки периодичности. 

Выберете категорию из представленных ниже, для настройки периодичности опросов, удаления или добавления определений.\
"""
    else:
        output = f"""
Категория "{category}"

Пожалуйста, укажите корректный часовой период, выбите подходящий вариант из списка:

{hours_map}"""
    return output






















'''def text_show_category(self, input_text):

        output_text = f"""
Выбрана  {input_text}"
                \n\nВыберите Категорию
        """
        return output_text'''
