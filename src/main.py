"""CLI: визуализация графа зависимостей (этап 1).

Минимальный прототип: чтение INI и вывод
параметров в формате ключ=значение.
"""

import argparse
import os
import sys

sys.path.insert(
    0, os.path.dirname(os.path.abspath(__file__))
)
from config_loader import load_config


def parse_args(argv=None):
    """Аргументы командной строки."""
    parser = argparse.ArgumentParser(
        description=(
            "Граф зависимостей пакетов (этап 1)"
        )
    )
    parser.add_argument(
        "-c",
        "--config",
        default="configs/config.ini",
        help="путь к INI-конфигу",
    )
    return parser.parse_args(argv)


def print_params(params):
    """Печать параметров ключ=значение."""
    print("=== Параметры конфигурации ===")
    for key in sorted(params.keys()):
        print(f"{key}={params[key]}")
    print("================================")


def run(argv=None):
    """Точка входа приложения."""
    args = parse_args(argv)
    try:
        params = load_config(args.config)
    except FileNotFoundError as err:
        print(f"[ERROR] {err}", file=sys.stderr)
        return 1
    except ValueError as err:
        print(f"[ERROR] {err}", file=sys.stderr)
        return 1
    print_params(params)
    return 0


def main():
    """Запуск с кодом выхода."""
    sys.exit(run())


if __name__ == "__main__":
    main()
