# cd /Users/denis/github/letuchka_bot/letuchka/def_base/management/commands
import time
import sqlite3
import asyncio
import calendar
import requests
from datetime import date
# from archive.example_settings import WEEKS_MAP, RUSSIAN_WEEK, HOURS_MAP
# from letuchka_bot.letuchka.def_base.management.commands.buttons_handler import WEEKS_MAP, RUSSIAN_WEEK, HOURS_MAP
from buttons_handler import WEEKS_MAP, RUSSIAN_WEEK, HOURS_MAP  # терминал так видит
from django.conf import settings


conn = sqlite3.connect('/Users/denis/github/letuchka_bot/letuchka/db.sqlite3')  # исправить для деплоя
cursor = conn.cursor()
tasks = []


def read_from_definition(profile_id, category, command, query_def='None'):
    try:
        sql = f"SELECT * FROM def_base_definition WHERE profile_id={profile_id} AND category='{category}'"
        output = []
        for row in cursor.execute(sql):
            if command == 'one':  # конкретное определение
                if query_def == str(row[0]):
                    header = row[3]
                    questions = row[5]
                    text = row[1]
                    return header, questions, text
            elif command == 'first':    # словарь из номеров первых сообщений
                definition_id = str(row[0])
                output.append(definition_id)
        return output
    except sqlite3.OperationalError:
        print('sqlite3.OperationalError')
        read_from_definition(profile_id, category, command, query_def='None')


def read_from_category(profile_id):
    try:
        sql = f"SELECT * FROM def_base_category WHERE profile_id={profile_id}"
        categories = []
        for row in cursor.execute(sql):     # (5, 'Тестовая', 4, '8, 6', '51')
            try:
                name_category = row[1]
                set_category = row[3]
                num_last_definition = row[4]
                categories.append([name_category, set_category, num_last_definition])
            except IndexError:
                return None, None, None
        return categories
    except sqlite3.OperationalError:
        print('sqlite3.OperationalError')
        read_from_category(profile_id)


def read_from_profiles():
    try:
        # get START
        id_ci_and_start = {}
        for row in cursor.execute("SELECT rowid, * FROM def_base_profile"):
            # (4, 4, 325655753, 'chame1e0n', "('working',)")
            id_ci_and_start.update({row[1]: [str(row[2]), row[4]]})
        return id_ci_and_start
    except sqlite3.OperationalError:
        print('sqlite3.OperationalError')
        read_from_profiles()


def write_category_last_definition(profile_id, name_category, the_definition_id):
    print('write_category_last_definition', the_definition_id, '\n', profile_id, name_category)
    sql = f"""
UPDATE def_base_category SET last_definition = {the_definition_id}
WHERE category = '{name_category}' AND profile_id = {profile_id}
     """
    print('READY')
    cursor.execute(sql)
    conn.commit()


def what_is_day(set_week):
    print('what_is_day')
    my_date = date.today()
    today_eng = calendar.day_name[my_date.weekday()]

    for i in RUSSIAN_WEEK:
        a = i.get(today_eng)
        if a:
            if WEEKS_MAP[int(set_week)] == a:   # проверяем входящие настройки(1, 1), тот ли сегодня день
                return a
            elif set_week == '8':  # ежедневно
                return 'ежедневно'
            elif set_week == '9':  # "понедельник, среда, пятница"
                mn_wd_fd = WEEKS_MAP[9].split()
                for j in mn_wd_fd:
                    j = j.replace(',', '')
                    if a == j:
                        return j
            elif set_week == '10':  # "понедельник, среда, пятница"
                mn_wd_fd = WEEKS_MAP[10].split()
                for j in mn_wd_fd:
                    j = j.replace(',', '')
                    if a == j:
                        return j


def what_is_hour(set_hour):
    # считываем настройки из словаря
    user_time = HOURS_MAP[int(set_hour)]
    # переводим условия в удобный для выполнения формат - в слиски через генераторы
    try_minutes = None
    try_time = None
    if set_hour == 1:       # 1 раз в день"
        try_time = ['12']
    elif set_hour == 2:     # утром, в обед и вечером
        try_time = ['09', '12', '18']
    elif set_hour == 3:     # каждые три часа
        try_time = ['09'] + [str(i) for i in range(12, 22, 3)]
    elif set_hour == 4:     # каждые два часа
        try_time = ['09'] + [str(i) for i in range(11, 22, 2)]
    elif set_hour == 5:      # каждый час
        try_time = ['09'] + [str(i) for i in range(10, 22, 1)]
    elif set_hour == 6:     # каждые пол часа
        try_minutes = True
        try_time = ['09'] + [str(i) for i in range(10, 23, 1)]  # 22

    # получем текущее время на сервере
    currently_time = time.strftime("%X", time.localtime())
    print('what_is_hour', currently_time)
    # сравниваем со временем из настроек
    hours, minutes = currently_time[0:5].replace(':', ' ').split()      # 09:45
    if hours in try_time:   # если часы есть в указанных часах
        # TODO: заменить таймер, и отправлять сообщение в один момент
        if try_minutes:      # если каждые тридцать минут
            # если разница в 10 минут - возвращаем точное время
            if minutes == '30':
                return hours, '30'
            elif minutes == '00':
                return hours, '00'
        elif minutes == '00':    # если все остальные почасовые варианты
            # если разница в 10 минут - возвращаем точное время
            print('return hours, 00')
            return hours, '00'
        else:
            print('ДРУГИЕ МИНУТЫ', 'user_time =', user_time)
            return
    else:
        print('ДРУГОЙ ЧАС', 'user_time =', user_time)
        return


async def try_settings():
    # раз в 1 минуту считываем настройки
    while True:
        print('try_settings while True')

        id_ci_and_start = read_from_profiles()    # возвращаются все профили с настройками,
        for p in id_ci_and_start:    # k - id_profile
            # (4, 4, 325655753, 'chame1e0n', "('working',)")
            # id_ci_and_start.update({row[1]: [str(row[2]), row[4]]})

            chat_id, start_is = id_ci_and_start[p]      # 325655753 ('working',)
            for x, y in ("('", ""), ("',)", ""):
                start_is = start_is.replace(x, y)
            if start_is == 'working':
                # start есть - передаем их дальше

                # категория, переодичность, и последнее выполненное определение
                for category in read_from_category(p):
                    name_category, set_category, num_last_definition = category
                    if name_category:
                        # получаем сегодняюнюю дату и время и сравниваем с тем что в словаре,
                        # сначала день недели, потом время
                        set_week, set_hour = set_category.split()
                        day = what_is_day(set_week.replace(',', ''))
                        if day:     # если тот день
                            print('____________', p, '____________')
                            try:    # если тот час
                                hour, minutes = what_is_hour(int(set_hour))
                                # тут лежит один профиль для обработки
                                ch_id_and_time = chat_id, hour, minutes
                                # номер последнего определения и категорию передаем
                                # в асинхронную функцию обработки определений
                                task = asyncio.create_task(preparation_definition(
                                    name_category,
                                    num_last_definition,
                                    p,
                                    ch_id_and_time))
                                tasks.append(task)

                            except TypeError as e:
                                error_message = f'what_is_hour НЕ ИЗВЛЕЧЕН: {e}'
                                print(error_message)
                        else:
                            print(f'\nУ ПРОФИЛЯ "{p}" НЕ ТОТ ДЕНЬ, ЕГО НАСТРОЙКИ: {set_category}\n')
                    else:
                        print(f'\nУ ПРОФИЛЯ "{p}" НЕТ КАТЕГОРИИ\n')
            else:
                print(f'\nПРОФИЛЬ {p} НЕ ЗАПУЩЕН\n')
        await asyncio.sleep(55)     # потом поменять на 45 чтобы небыло пропусков


# запускаем отдельный поток, считываем из базы нужную информацию и передаем таймеру
async def preparation_definition(name_category, num_last_definition, profile_id, ch_id_and_time):
    """
    :param name_category: имя категории
    :param num_last_definition: последнее определение
    :param profile_id: номер профился
    :param ch_id_and_time: chat_id и времея
    :return: возвращает только асинхронную задачу
    """
    # while True:   # здесь не нужен цикл, просто подготовка определения
    print('preparation_definition')
    all_definition_id = read_from_definition(profile_id, name_category, 'first')
    # the_definition_id = None
    # если последнего определения нет, берем первое из определений
    if num_last_definition == 'None':
        the_definition_id = all_definition_id[0]    # берем первое

    # все определения и среди них ищем последнее, считываем следующее.
    else:
        if num_last_definition in all_definition_id:
            count = 0
            for i in all_definition_id:
                count += 1
                if i == num_last_definition:    # если в словаре с определениями находится последнее определение
                    # нужно проверить
                    # иначе переходим на первый элемент
                    if len(all_definition_id) > count:     # если элементов в словаре больше чем следующий элемент
                        the_definition_id = all_definition_id[count]    # берем следующее
                    else:
                        the_definition_id = all_definition_id[0]    # берем первое

    # передаем номер определения для отправки в таймер
    task = asyncio.create_task(timer(the_definition_id, ch_id_and_time, profile_id, name_category))
    tasks.append(task)


# отправляем определение и записываем в категории новое последнее определение
async def timer(the_definition_id, ch_id_and_time, profile_id, name_category):
    """
    :param the_definition_id: номер определения для работы
    :param ch_id_and_time: chat_id и времея
    :param profile_id: номер профился
    :param name_category: имя категории
    :return: возвращает только асинхронную задачу
    """
    # while True: # уже есть цикл
    print('timer')
    # сохраняем номер текущего определения в last_definition

    # ждем время
    chat_id, hours_start, minutes_start = ch_id_and_time
    count = 0
    while True:
        currently_time = time.strftime("%X", time.localtime())
        currently_hours, currently_minutes = currently_time[0:5].replace(':', ' ').split()      # 09:45
        if currently_hours == hours_start:  # если сейчас тот же час что и час старта

            if count == 0 and currently_minutes == minutes_start:  # если сейчас та же минута что и минута старта
                write_category_last_definition(profile_id, name_category, the_definition_id)
                print('currently_minutes == minutes_start', int(currently_minutes), int(minutes_start))
                count += 1
                # достаем из базы все про текущее определение
                header, question, text = read_from_definition(profile_id, name_category, 'one', the_definition_id)

                # формируем запрос и отправляем на серввер
                message_text = f'Ответьте на вопрос из категории "{name_category}":\n\n"{question}"'
                tasks.append(await asyncio.create_task(send_message(chat_id, message_text)))
                break
            else:
                # print('timer ждет time.sleep(1) потому что не та минута')
                time.sleep(1)

        else:
            print('timer ждет time.sleep(360) потому что не тот час')
            time.sleep(360)


async def send_message(chat_id, message_text):
    print('send message')
    # tg_token = '1163241015:AAHVLDANNrcw6QDs4pALZcLSKt57bOpCOG0'

    foundation_url = "https://telegg.ru/orig/bot" + settings.TG_TOKEN
    url = foundation_url + f"/sendmessage?chat_id={chat_id}&text={message_text}"
    requests.get(url)


async def main():
    tasks.append(asyncio.create_task(try_settings()))
    await asyncio.gather(*tasks)


if __name__ == '__main__':
    asyncio.run(main())






