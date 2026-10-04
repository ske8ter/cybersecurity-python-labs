"""Завдання 3: Хешування, CSV-база користувачів та JSON-логування."""

import csv
import datetime
import functools
import hashlib
import json
import os
import random
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from shared.student import VARIANT_NUMBER

MIN_PASS_LENGTH = 11
SALT = f"{VARIANT_NUMBER:05d}"

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
USERS_CSV = os.path.join(DATA_DIR, "users.csv")
LOG_JSON = os.path.join(DATA_DIR, "log.json")

users_to_register = (
    ("ada_lovelace", "l#1"),
    ("alan_turing", "EnigmaBreaker!"),
    ("grace_hopper", "CompilerBug99"),
    ("linus_torvalds", "GitMaster2026!"),
    ("margaret_ham", "ApolloCode11!"),
    ("tim_berners", "WorldWideWeb3"),
    ("guido_vanrossum", "PythonSnake!3"),
    ("richard_stallman", "FreeSoftware#"),
    ("dennis_ritchie", "C_Language99!"),
    ("bjarne_stroustrup", "CPlusPlusRule!"),
)

users_db = []


class ValidationError(Exception):
    """Пароль не відповідає вимогам безпеки."""

    def __init__(self):
        super().__init__(
            f"Password must be at least {MIN_PASS_LENGTH} characters long."
        )


def generate_hash(password: str, salt: str = "00000") -> str:
    """Повертає SHA-256 хеш конкатенації пароля та солі."""
    if not password or not salt:
        raise ValueError("Password and salt must not be empty.")
    if len(password) < MIN_PASS_LENGTH:
        raise ValidationError

    data = (password + salt).encode("utf-8")
    return hashlib.sha256(data).hexdigest()


def create_user(username, password):
    """Повертає кортеж (username, hash_value) з персональною сіллю."""
    return (username, generate_hash(password, SALT))


def create_users(users_list):
    """Записує базу користувачів у data/users.csv."""
    os.makedirs(DATA_DIR, exist_ok=True)
    users = []
    for username, password in users_list:
        try:
            users.append(create_user(username, password))
        except ValidationError as error:
            print(f"[!] User: {username} => {error}")

    with open(USERS_CSV, mode="w", newline="", encoding="utf-8") as file:
        csv.writer(file).writerows(users)


def read_users():
    """Зчитує базу користувачів з data/users.csv."""
    with open(USERS_CSV, mode="r", encoding="utf-8") as file:
        return [row for row in csv.reader(file) if row]


def print_users_table(db):
    """Виводить базу користувачів у вигляді таблиці."""
    print(f"{'Username':<20} | {'SHA-256':<64}")
    print("-" * 20 + "-+-" + "-" * 64)
    for username, hash_value in db:
        print(f"{username:<20} | {hash_value}")


def log_event(func):
    """Декоратор: записує кожну спробу входу у data/log.json."""

    @functools.wraps(func)
    def wrapper(username, password, *args, **kwargs):
        success = func(username, password, *args, **kwargs)

        timezone = datetime.timezone(datetime.timedelta(hours=3))
        now = datetime.datetime.now(timezone)

        os.makedirs(DATA_DIR, exist_ok=True)
        logs = []
        if os.path.exists(LOG_JSON) and os.path.getsize(LOG_JSON) > 0:
            with open(LOG_JSON, "r", encoding="utf-8") as file:
                logs = json.load(file)

        logs.append(
            {
                "event": "login",
                "user": username,
                "result": "success" if success else "failure",
                "timestamp": now.strftime("%Y-%m-%d %H:%M:%S"),
                "args": list(args),
                "kwargs": kwargs,
            }
        )

        with open(LOG_JSON, "w", encoding="utf-8") as file:
            json.dump(logs, file, indent=4, ensure_ascii=False)

        return success

    return wrapper


@log_event
def login(username: str, password: str) -> bool:
    """Перевіряє логін і пароль за базою users_db."""
    if not username or not password:
        raise ValueError("Username and password must not be empty.")

    hash_value = generate_hash(password, SALT)
    return [username, hash_value] in users_db


def run_task3():
    """Реєстрація, читання бази та автентифікація користувача."""
    try:
        create_users(users_to_register)
        users_db[:] = read_users()
        print_users_table(users_db)

        registered = {row[0] for row in users_db}
        candidates = [u for u in users_to_register if u[0] in registered]
        username, password = random.choice(candidates)

        success = login(username, password)
        print(f"\nlogin({username}) -> {'success' if success else 'failure'}")

    except (
        OSError,
        FileNotFoundError,
        PermissionError,
        ValidationError,
        ValueError,
    ) as error:
        print(f"[!] {error}")


def main():
    """Головна функція завдання 3."""
    run_task3()


if __name__ == "__main__":
    main()
