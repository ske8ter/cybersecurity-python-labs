"""Завдання 1: Комплексний аналізатор надійності паролів."""

import os
import random
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from shared.student import STUDENT_NAME, VARIANT_NUMBER

passwords = [
    "ThreatH@nt3r",
    "weak123",
    "P3n3trat10n@Test",
    "visitor",
    "Cyber@Defense2023",
    "normal",
    "Incident@R3sp0nse",
    "standard",
    "Risk@Analys1s",
    "typical",
]

criteria = {
    "min_length": 10,
    "require_digits": True,
    "require_upper": True,
    "require_special": True,
}

forbidden_passwords = {
    "weak123",
    "visitor",
    "normal",
    "standard",
    "typical",
    "admin",
}

DUPLICATES_COUNT = 3
VERY_STRONG_EXTRA = 4


def add_duplicates(pw_list, count=DUPLICATES_COUNT):
    """Додає в кінець списку дублікати паролів з випадкових індексів."""
    indexes = random.sample(range(len(pw_list)), count)
    return pw_list + [pw_list[i] for i in indexes]


def meets_all_criteria(password):
    """Перевіряє довжину, цифру, велику літеру та спецсимвол."""
    checks = [len(password) >= criteria["min_length"]]
    if criteria["require_digits"]:
        checks.append(any(char.isdigit() for char in password))
    if criteria["require_upper"]:
        checks.append(any(char.isupper() for char in password))
    if criteria["require_special"]:
        checks.append(any(not char.isalnum() for char in password))
    return all(checks)


def count_groups(password):
    """Рахує, скільки груп символів (a-z, A-Z, 0-9, спецсимволи) є в паролі."""
    groups = (
        any(char.islower() for char in password),
        any(char.isupper() for char in password),
        any(char.isdigit() for char in password),
        any(not char.isalnum() for char in password),
    )
    return sum(groups)


def rate_password(password, all_passwords):
    """Повертає оцінку надійності пароля."""
    if password in forbidden_passwords or len(password) < criteria["min_length"]:
        return "Forbidden"

    if meets_all_criteria(password):
        is_long = len(password) >= criteria["min_length"] + VERY_STRONG_EXTRA
        if is_long and all_passwords.count(password) == 1:
            return "Very strong"
        return "Strong"

    if count_groups(password) >= 2:
        return "Medium"

    return "Weak"


def print_table(rows):
    """Виводить результати аналізу у вигляді таблиці."""
    header = f"{'#':<3} | {'Password':<20} | {'Len':<3} | Status"
    print(header)
    print("-" * len(header))
    for number, (password, status) in enumerate(rows, start=1):
        print(f"{number:<3} | {password:<20} | {len(password):<3} | {status}")


def run_task1():
    """Запускає аналіз надійності паролів."""
    print(f"\nЗавдання 1 | {STUDENT_NAME} | варіант {VARIANT_NUMBER}")
    all_passwords = add_duplicates(passwords)
    rows = [(pw, rate_password(pw, all_passwords)) for pw in all_passwords]
    print_table(rows)


if __name__ == "__main__":
    run_task1()
