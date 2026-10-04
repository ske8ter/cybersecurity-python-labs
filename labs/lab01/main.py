"""Лабораторна робота №1: головний файл для демонстрації роботи."""

import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from labs.lab01.task1 import run_task1
from labs.lab01.task2 import run_task2
from labs.lab01.task3 import run_task3
from shared.student import GROUP_NAME, STUDENT_NAME, VARIANT_NUMBER


def main():
    """Запускає всі завдання лабораторної роботи."""
    print(f"{STUDENT_NAME}\n{GROUP_NAME}\n{VARIANT_NUMBER}")
    run_task1()
    run_task2()
    run_task3()


if __name__ == "__main__":
    main()
