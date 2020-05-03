# Crutch for module from top directory
import sys
sys.path.append('/users/denis/github/letuchka_bot/letuchka/')
from def_base.models import Profile
from def_base.models import Definition
from def_base.models import Category


def profile(update, chat_id):
    p, _ = Profile.objects.get_or_create(
            external_id=chat_id,
            defaults={
                'name': update.message.from_user.username,
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


def read_from_base(g_id):
    """count = Category.filter(profile=p).count()
    return count"""
    """categories = Category.category
    return categories"""
    # id_profile = Profile.objects.get(external_id=external_id)
    whole_base = Category.objects.filter(profile=g_id)
    return whole_base


def write_to_category(p, text):
    c = Category(
        profile=p,
        category=text,
    )
    c.save()

    """c = Category(
        category='test_category',
    )
    c.save()"""

    """chat_id = update.message.chat_id
    p, _ = Profile.objects.get_or_create(
        external_id=chat_id,
        defaults={
            'name': update.message.from_user.username,
        }
    )
    count = Message.objects.filter(profile=p).count()

    update.message.reply_text(
        text=f'У вас {count} сообщений',
    )"""


def main():
    # print(read_from_base(write_to_base('325655753')))
    pass

if __name__ == '__main__':
    main()
