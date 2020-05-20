from typing import Optional


WEEKS_MAP = {
    1: "понедельник",
    2: "вторник",
    3: "среда",
    4: "четверг",
    5: "пятница",
    6: "суббота",
    7: "воскресенье",
    8: "ежедневно",
    9: "суббота, воскресенье",
    10: "понедельник, среда, пятница",
}

RUSSIAN_WEEK = [
        {'Monday': 'понедельник'},
        {'Tuesday': 'вторник'},
        {'Wednesday': 'среда'},
        {'Thursday': 'четверг'},
        {'Friday': 'пятница'},
        {'Saturday': 'суббота'},
        {'Sunday': 'воскресенье'},
    ]

HOURS_MAP = {
    1: "1 раз в день",
    2: "утром, в обед и вечером",
    3: "каждые три часа",
    4: "каждые два часа",
    5: "каждый час",
    6: "каждые пол часа",
}


def validate_weeks(text: str) -> Optional[int]:
    try:
        weeks = int(text)
    except (TypeError, ValueError):
        return None
    if weeks in WEEKS_MAP:
        return weeks


def validate_hours(text: str) -> Optional[int]:
    try:
        hours = int(text)
    except (TypeError, ValueError):
        return None
    if hours in HOURS_MAP:
        return hours

