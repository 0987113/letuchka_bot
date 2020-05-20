# Crutch for module from top directory
import sys
import sqlite3
import traceback
from .buttons_handler import WEEKS_MAP, HOURS_MAP

sys.path.append('///home/tele/letuchka_bot/letuchka/')
from def_base.models import Profile
from def_base.models import Definition
from def_base.models import Category


def log_uncaught_exceptions(ex_cls, ex, tb):
    text = '{}: {}:\n'.format(ex_cls.__name__, ex)
    text += ''.join(traceback.format_tb(tb))

    print(text)
    # Или


sys.excepthook = log_uncaught_exceptions


def profile(update, chat_id):
    try:
        try:
            print('profile')
            p, _ = Profile.objects.get_or_create(
                    external_id=chat_id,
                    defaults={
                        'name': update.message.from_user.username,
                    }
                )
        except AttributeError:
            p, _ = Profile.objects.get_or_create(
                external_id=chat_id,
                defaults={
                    'name': update.callback_query.message.chat.username,
                }
            )
        return p, _
    except:
        profile(update, chat_id)


def write_to_profile_start(p, comm):
    try:
        print('write_to_profile_start')
        p2 = int(str(p))
        prof = Profile.objects.get(
            id=p2,
        )
        prof.start = comm,
        prof.save()
    except:
        write_to_profile_start(p, comm)


def read_from_category(p):
    try:
        print('read_from_category')
        whole_base = Category.objects.filter(profile=p)
        return whole_base
    except:
        read_from_category(p)


def read_from_category_set(p, category, command):
    try:
        print('read_from_category_set')
        c = Category.objects.get(
            profile=p,
            category=category,
        )
        if command == 'text_result':
            try_var = c.set_category  # 8, 5
            list_try_var = try_var.split()
            list_try_var_2 = [int(i.replace(',', '')) for i in list_try_var]
            output = f'неделя: "{WEEKS_MAP[int(list_try_var_2[0])]}", в течении дня: "{HOURS_MAP[int(list_try_var_2[1])]}"'
        else:
            return c.set_category
        return output
    except:
        read_from_category_set(p, category, command)


def write_to_name_category(p, text):
    try:
        print('write_to_name_category', text)
        c = Category(
            profile=p,
            category=text,
        )
        c.save()
    except:
        write_to_name_category(p, text)


def write_to_set_category(p, category, set_category):
    try:
        print('write_to_set_category')
        # In the category to change the parameters
        c = Category.objects.get(
            profile=p,
            category=category
        )
        c.set_category = set_category
        c.save()
    except:
        write_to_set_category(p, category, set_category)


def delete_category(p, text):
    try:
        print('delete_category', text)
        Category.objects.filter(profile=p, category=text).delete()
        Definition.objects.filter(profile=p, category=text).delete()
    except:
        delete_category(p, text)


def write_to_definitions(p, category,  text, header, question):
    try:
        print('write_to_definitions', text)
        d = Definition(
            profile=p,
            category=category,
            text=text,
            header=header,
            question=question,
        )
        d.save()
    except:
        write_to_definitions(p, category, text, header, question)


def read_from_definitions(p, category):
    try:
        print('read_from_definitions')
        whole_base = Definition.objects.filter(profile=p, category=category)
        return whole_base
    except:
        read_from_definitions(p, category)


def read_from_definitions_data(p, category, definition):
    try:
        print('read_from_definitions_data')
        d = Definition.objects.get(
            profile=p,
            category=category,
            header=definition,
        )
        return d.text, d.question
    except:
        read_from_definitions_data(p, category, definition)


def delete_definition(p, header):
    try:
        print('delete_definition', header)
        Definition.objects.filter(profile=p, header=header).delete()
    except:
        delete_definition(p, header)

