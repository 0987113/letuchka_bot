from telegram import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup


def get_buttons_cd(buttons: list):
    # TODO: One function and two buttons on the row
    print('get_buttons:', len(buttons))
    keyboard = []
    button_add = InlineKeyboardButton('<Добавить>', callback_data='__<ADD>__')
    if len(buttons) <= 3:
        keyboard_into = []
        for i in range(len(buttons)):
            button = InlineKeyboardButton(f'{buttons[i]}', callback_data=f'{buttons[i]}')
            keyboard_into.append(button)
        keyboard_into.append(button_add)
        keyboard.append(keyboard_into)
    elif 12 >= len(buttons) > 3:
        total_count = 0
        while len(buttons) > total_count:  # and count < 3:
            count = 0
            keyboard_into = []
            while count < 3 and total_count < len(buttons):
                button = InlineKeyboardButton(f'{buttons[total_count]}', callback_data=f'{buttons[total_count]}')
                keyboard_into.append(button)
                count += 1
                total_count += 1
            keyboard_into.append(button_add)
            keyboard.append(keyboard_into)
    return InlineKeyboardMarkup(keyboard)


def get_keyboard_into(buttons: list):
    print('get_keyboard_into:', len(buttons))
    keyboard = []
    if len(buttons) <= 2:
        keyboard_into = []
        for i in range(len(buttons)):
            button = InlineKeyboardButton(f'{buttons[i]}', callback_data=f'{buttons[i]}')
            keyboard_into.append(button)
        keyboard.append(keyboard_into)
    elif 8 >= len(buttons) > 2:
        total_count = 0
        while len(buttons) > total_count:
            count = 0
            keyboard_into = []
            while count < 2 and total_count < len(buttons):
                button = InlineKeyboardButton(f'{buttons[total_count]}', callback_data=f'{buttons[total_count]}')
                keyboard_into.append(button)
                count += 1
                total_count += 1
            keyboard.append(keyboard_into)
    return InlineKeyboardMarkup(keyboard)
