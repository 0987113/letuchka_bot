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


def ready_buttons(n: int, buttons: list):
    """
    Нужно вернуть определенное колличество кнопок с определенными первичными ключами
    :param n:
    :param buttons:
    :return:
    """
    count = 0
    """buttons_one = [InlineKeyboardButton(f'{buttons[n]}', callback_data=f'{buttons[n]}')]

    buttons_two = [InlineKeyboardButton(f'{buttons[n]}', callback_data=f'{buttons[n]}'),
                   InlineKeyboardButton(f'{buttons[n]}', callback_data=f'{buttons[n]}')]

    buttons_three = [InlineKeyboardButton(f'{buttons[n]}', callback_data=f'{buttons[n]}'),
                     InlineKeyboardButton(f'{buttons[n]}', callback_data=f'{buttons[n]}'),
                     InlineKeyboardButton(f'{buttons[n]}', callback_data=f'{buttons[n]}')]"""
    ready_but = [
            [InlineKeyboardButton(f'{buttons[n]}', callback_data=f'{buttons[n]}')],

            [InlineKeyboardButton(f'{buttons[n]}', callback_data=f'{buttons[n]}'),
             InlineKeyboardButton(f'{buttons[n]}', callback_data=f'{buttons[n]}')],

            [InlineKeyboardButton(f'{buttons[n]}', callback_data=f'{buttons[n]}'),
             InlineKeyboardButton(f'{buttons[n]}', callback_data=f'{buttons[n]}'),
             InlineKeyboardButton(f'{buttons[n]}', callback_data=f'{buttons[n]}')],
        ]
    control_num = len(buttons)[0::3]
    print(control_num)
    while buttons and 3 >= len(buttons) > count:
        count += 1
        keyboard = [ready_but[len(buttons)-1]]
    while 6 >= len(buttons) > 3:
        pass
    while 9 >= len(buttons) > 6:
        pass
    while 12 >= len(buttons) > 9:
        pass

    ready_but = ''
    return ready_but


def get_buttons(buttons: list):
    print('get_buttons:', len(buttons))
    # num_buttons = [i for i in range(1, 10)]
    # 3 - Создаем переменную с клавиатурой и кнопками
    """
    Привзываемся к колличеству категорий, до 12 например
    """
    n = 1
    ready_but = ready_buttons(n, buttons)

    if buttons and len(buttons) <= 3:
        print('IF_1')
        keyboard = [ready_but[len(buttons)-1]]
    elif 6 >= len(buttons) > 3:
        print('IF_2')
        keyboard = [ready_but[len(buttons)-1], ready_but[len(buttons)-1]]
    elif 9 >= len(buttons) > 6:
        print('IF_3')
        keyboard = [ready_but[len(buttons)-1], ready_but[len(buttons)-1], ready_but[len(buttons)-1]]
    elif 12 >= len(buttons) > 9:
        print('IF_4')
        keyboard = [
            ready_but[len(buttons)-1],
            ready_but[len(buttons)-1],
            ready_but[len(buttons)-1],
            ready_but[len(buttons)-1],
        ]

        """if len(buttons) == 1:
            keyboard = [[InlineKeyboardButton(f'{buttons[0]}', callback_data=f'{buttons[0]}')]]
        elif len(buttons) == 2:
            keyboard = [[InlineKeyboardButton(f'{buttons[0]}', callback_data=f'{buttons[0]}'),
                        InlineKeyboardButton(f'{buttons[1]}', callback_data=f'{buttons[1]}')]]"""
    else:
        pass
        """keyboard = [[InlineKeyboardButton(f'{buttons[0]}', callback_data=f'{buttons[0]}'),
                     InlineKeyboardButton(f'{buttons[1]}', callback_data=f'{buttons[1]}'),
                     InlineKeyboardButton(f'{buttons[2]}', callback_data=f'{buttons[2]}')]]
        print('___________________\n', keyboard)"""
    a = InlineKeyboardMarkup(keyboard)
    return a


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

    """elif len(buttons) == 3:
            keyboard = [[(InlineKeyboardButton(f'{buttons[0]}', callback_data=f'{num_buttons[2]}')),
                         (InlineKeyboardButton(f'{buttons[1]}', callback_data=f'{num_buttons[2]}')),
                         (InlineKeyboardButton(f'{buttons[2]}', callback_data=f'{num_buttons[2]}'))
                         ]]
        elif len(buttons) == 4:
            keyboard = [[(InlineKeyboardButton(f'{buttons[0]}', callback_data=f'{num_buttons[2]}')),
                         (InlineKeyboardButton(f'{buttons[1]}', callback_data=f'{num_buttons[2]}')),
                         (InlineKeyboardButton(f'{buttons[2]}', callback_data=f'{num_buttons[2]}'))
                         ],
                        [
                            (InlineKeyboardButton(f'{buttons[3]}', callback_data=f'{num_buttons[2]}'))
                        ]]
        elif len(buttons) == 5:
            keyboard = [[(InlineKeyboardButton(f'{buttons[0]}', callback_data=f'{num_buttons[2]}')),
                         (InlineKeyboardButton(f'{buttons[1]}', callback_data=f'{len(buttons)-3}')),
                         (InlineKeyboardButton(f'{buttons[2]}', callback_data=f'{len(buttons)-2}'))
                         ],
                        [
                            (InlineKeyboardButton(f'{buttons[3]}', callback_data=f'{len(buttons)-1}')),
                            (InlineKeyboardButton(f'{buttons[4]}', callback_data=f'{len(buttons)}'))
                        ]]
        elif len(buttons) == 6:
            keyboard = [[(InlineKeyboardButton(f'{buttons[0]}', callback_data=f'{len(buttons)-5}')),
                         (InlineKeyboardButton(f'{buttons[1]}', callback_data=f'{len(buttons)-4}')),
                         (InlineKeyboardButton(f'{buttons[2]}', callback_data=f'{len(buttons)-3}'))
                         ],
                        [
                            (InlineKeyboardButton(f'{buttons[3]}', callback_data=f'{len(buttons)-2}')),
                            (InlineKeyboardButton(f'{buttons[4]}', callback_data=f'{len(buttons)-1}')),
                            (InlineKeyboardButton(f'{buttons[5]}', callback_data=f'{len(buttons)}'))
                        ]]
        elif len(buttons) == 7:
            keyboard = [
                        [(InlineKeyboardButton(f'{buttons[0]}', callback_data=f'{len(buttons)-5}')),
                         (InlineKeyboardButton(f'{buttons[1]}', callback_data=f'{len(buttons)-4}')),
                         (InlineKeyboardButton(f'{buttons[2]}', callback_data=f'{len(buttons)-3}'))
                         ],
                        [(InlineKeyboardButton(f'{buttons[3]}', callback_data=f'{len(buttons)-2}')),
                         (InlineKeyboardButton(f'{buttons[4]}', callback_data=f'{len(buttons)-1}')),
                         (InlineKeyboardButton(f'{buttons[5]}', callback_data=f'{len(buttons)}')),
                         ],
                        [(InlineKeyboardButton(f'{buttons[0]}', callback_data=f'{len(buttons) - 5}'))
                         ]]
        elif len(buttons) == 8:
            keyboard = [[(InlineKeyboardButton(f'{buttons[0]}', callback_data=f'{len(buttons)-5}')),
                         (InlineKeyboardButton(f'{buttons[1]}', callback_data=f'{len(buttons)-4}')),
                         (InlineKeyboardButton(f'{buttons[2]}', callback_data=f'{len(buttons)-3}'))
                         ],
                        [
                            (InlineKeyboardButton(f'{buttons[3]}', callback_data=f'{len(buttons)-2}')),
                            (InlineKeyboardButton(f'{buttons[4]}', callback_data=f'{len(buttons)-1}')),
                            (InlineKeyboardButton(f'{buttons[5]}', callback_data=f'{len(buttons)}'))
                        ],
                        [
                            (InlineKeyboardButton(f'{buttons[3]}', callback_data=f'{len(buttons)-2}')),
                            (InlineKeyboardButton(f'{buttons[4]}', callback_data=f'{len(buttons)-1}'))
                        ]]
        elif len(buttons) == 9:
            keyboard = [[(InlineKeyboardButton(f'{buttons[0]}', callback_data=f'{len(buttons)-5}')),
                         (InlineKeyboardButton(f'{buttons[1]}', callback_data=f'{len(buttons)-4}')),
                         (InlineKeyboardButton(f'{buttons[2]}', callback_data=f'{len(buttons)-3}'))
                         ],
                        [
                            (InlineKeyboardButton(f'{buttons[3]}', callback_data=f'{len(buttons)-2}')),
                            (InlineKeyboardButton(f'{buttons[4]}', callback_data=f'{len(buttons)-1}')),
                            (InlineKeyboardButton(f'{buttons[5]}', callback_data=f'{len(buttons)}'))
                        ],
                        [
                            (InlineKeyboardButton(f'{buttons[3]}', callback_data=f'{len(buttons) - 2}')),
                            (InlineKeyboardButton(f'{buttons[4]}', callback_data=f'{len(buttons) - 1}')),
                            (InlineKeyboardButton(f'{buttons[5]}', callback_data=f'{len(buttons)}'))
                        ]]
        elif len(buttons) == 10:
            keyboard = [[(InlineKeyboardButton(f'{buttons[0]}', callback_data=f'{len(buttons)-5}')),
                         (InlineKeyboardButton(f'{buttons[1]}', callback_data=f'{len(buttons)-4}')),
                         (InlineKeyboardButton(f'{buttons[2]}', callback_data=f'{len(buttons)-3}'))
                         ],
                        [
                            (InlineKeyboardButton(f'{buttons[3]}', callback_data=f'{len(buttons)-2}')),
                            (InlineKeyboardButton(f'{buttons[4]}', callback_data=f'{len(buttons)-1}')),
                            (InlineKeyboardButton(f'{buttons[5]}', callback_data=f'{len(buttons)}'))
                        ],
                        [
                            (InlineKeyboardButton(f'{buttons[3]}', callback_data=f'{len(buttons) - 2}')),
                            (InlineKeyboardButton(f'{buttons[4]}', callback_data=f'{len(buttons) - 1}')),
                            (InlineKeyboardButton(f'{buttons[5]}', callback_data=f'{len(buttons)}'))
                        ],
                        [
                            (InlineKeyboardButton(f'{buttons[3]}', callback_data=f'{len(buttons) - 2}'))
                ]]"""
