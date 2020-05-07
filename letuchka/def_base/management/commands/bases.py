# Crutch for module from top directory
import sys
sys.path.append('/users/denis/github/letuchka_bot/letuchka/')
from def_base.models import Profile
from def_base.models import Definition
from def_base.models import Category


def profile(update, chat_id):
    try:
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


def definition(p, text):
    d = Definition(
        profile=p,
        text=text,
        header_def='The_header',
    )
    d.save()


def read_from_category(p):
    whole_base = Category.objects.filter(profile=p)
    return whole_base


def write_to_category(p, text):
    c = Category(
        profile=p,
        category=text,
    )
    c.save()


def delete_category(p, text):
    print('delete_category', text)
    c = Category.objects.filter(profile=p, category=text).delete()


