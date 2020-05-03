from telegram import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup


def log_errors(f):

    def inner(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            error_message = f'Ошибка: {e}___{f}'
            print(error_message)
            raise e
    return inner


def get_buttons(buttons: list):
    # TODO: Button del
    print('get_buttons:', len(buttons), buttons)
    keyboard = []
    if len(buttons) <= 3:
        keyboard_into = []
        for i in range(len(buttons)):
            button = InlineKeyboardButton(f'{buttons[i]}', callback_data=f'{buttons[i]}')
            keyboard_into.append(button)
        keyboard.append(keyboard_into)
    elif 12 >= len(buttons) > 3:
        total_count = 0
        while len(buttons) > total_count:  # and count < 3:
            count = 0
            keyboard_into = []
            while count < 3 and total_count < len(buttons):
                print(total_count, count)
                button = InlineKeyboardButton(f'{buttons[total_count]}', callback_data=f'{buttons[total_count]}')
                keyboard_into.append(button)
                count += 1
                total_count += 1
            keyboard.append(keyboard_into)
    return InlineKeyboardMarkup(keyboard)


CATEGORIES = "Категории"
NEW_CATEGORY = "Новая"
DEL_CATEGORY = "Удалить"


@log_errors
def get_keyboard_category():
    keyboard = [
        [
            KeyboardButton(CATEGORIES),
            KeyboardButton(NEW_CATEGORY),
            KeyboardButton(DEL_CATEGORY),
        ],
    ]
    reply_markup = ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True,
    )
    return reply_markup
