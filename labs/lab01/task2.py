"""Завдання 2: Багаторівнева система контролю доступу."""

import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from shared.student import STUDENT_NAME, VARIANT_NUMBER

users = {
    "crypto_specialist": {
        "role": "cryptographer",
        "clearance": 4,
        "department": "Cryptography",
        "active": True,
    },
    "privacy_officer": {
        "role": "privacy_analyst",
        "clearance": 3,
        "department": "Privacy",
        "active": True,
    },
    "data_scientist": {
        "role": "data_analyst",
        "clearance": 2,
        "department": "Analytics",
        "active": True,
    },
    "field_engineer": {
        "role": "field_support",
        "clearance": 2,
        "department": "Field Ops",
        "active": True,
    },
    "test_account": {
        "role": "testing",
        "clearance": 1,
        "department": "QA",
        "active": False,
    },
}

resources = [
    ("encryption_keys", 4),
    ("privacy_policies", 3),
    ("anonymized_data", 2),
    ("field_reports", 2),
    ("crypto_algorithms", 4),
    ("consent_forms", 1),
    ("data_classification", 3),
    ("key_management", 4),
    ("statistical_models", 2),
    ("public_datasets", 1),
]

security_levels = ("Unclassified", "For Official Use", "Confidential", "Secret")

blocked_users = {"test_account", "gdpr_violation", "data_breach_user"}


def level_name(level):
    """Повертає текстову назву рівня безпеки (1-4) з security_levels."""
    return security_levels[level - 1]


def check_access(username, resource_level):
    """Повертає (дозволено, причина відмови) для користувача і ресурсу."""
    if username not in users:
        return False, "User not found"
    if username in blocked_users:
        return False, "User is blocked"

    user = users[username]
    if not user.get("active"):
        return False, "Account inactive"
    if user["clearance"] >= resource_level:
        return True, ""
    return False, "Insufficient clearance"


def print_resources():
    """Виводить ресурси з текстовими назвами рівнів безпеки."""
    print("Ресурси системи:")
    for name, level in resources:
        print(f"  {name:<22} {level_name(level)}")


def run_task2():
    """Перевіряє доступ кожного користувача до кожного ресурсу."""
    print(f"\nЗавдання 2 | {STUDENT_NAME} | варіант {VARIANT_NUMBER}")
    print_resources()

    # blocked_users може містити імена, яких немає в users ("User not found")
    all_users = list(users) + sorted(blocked_users - set(users))

    for username in all_users:
        print("-" * 60)
        print(f"Таблиця дозволів для {username}")
        for name, level in resources:
            allowed, reason = check_access(username, level)
            verdict = "ALLOW" if allowed else f"DENY ({reason})"
            print(f"user={username} resource={name} -> {verdict}")


if __name__ == "__main__":
    run_task2()
