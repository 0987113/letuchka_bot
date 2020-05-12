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


def read_from_category(p):
    whole_base = Category.objects.filter(profile=p)
    return whole_base


def write_to_name_category(p, text):
    c = Category(
        profile=p,
        category=text,
    )
    c.save()


def write_to_set_category(p, category, set_category):
    print('write_to_set_category', p, category, set_category)
    # In the category to change the parameters
    c = Category.objects.get(
        profile=p,
        category=category
    )
    c.set_category = set_category
    c.save()


def delete_category(p, text):
    print('delete_category', text)
    Category.objects.filter(profile=p, category=text).delete()
    Definition.objects.filter(profile=p, category=text).delete()


def write_to_definitions(p, category,  text, header, question):
    print('write_to_definitions', text)
    d = Definition(
        profile=p,
        category=category,
        text=text,
        header=header,
        question=question,
    )
    d.save()


def read_from_definitions(p, category):
    whole_base = Definition.objects.filter(profile=p, category=category)
    return whole_base


def delete_definition(p, header):
    print('delete_definition', header)
    Definition.objects.filter(profile=p, header=header).delete()

