from typing import Optional
from .bases import profile
from .keyboards import get_keyboard_into


WEEKS_MAP = {
    1: "ежедневно",
    2: "понедельник",
    3: "вторник",
    4: "среда",
    5: "четверг",
    6: "пятница",
    7: "понедельник, среда и пятница",
}

HOURS_MAP = {
    1: "1 раз",
    2: " утром, в обед и вечером",
    3: "каждый час",
    4: "каждые пол часа",
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

