"""CLI: граф зависимостей (этап 1).

Минимальный прототип: чтение INI и вывод
параметров в формате ключ=значение.
"""

import argparse
import os
import sys

from ascii_tree import render_tree
from cargo_deps import direct_dependencies
from config_loader import load_config
from graph_bfs import bfs_iterative, load_test_repo
from mermaid import describe
from order_topo import load_order
from pngimg import write_png


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


def run_test_graph(params):
    """Тестовый режим: граф из файла, обход в ширину (этапы 3-5)."""
    graph = load_test_repo(params["repo_url"])
    order, cycles = bfs_iterative(params["package_name"], graph.get)
    print("=== Порядок обхода ===")
    for name in order:
        print(name)
    if cycles:
        print("=== Циклы ===")
        for found in cycles:
            print(" -> ".join(found))
    print("=== Порядок загрузки ===")
    for name in load_order(params["package_name"], graph.get):
        print(name)
    print("=== Mermaid ===")
    print(describe(graph))
    if params["ascii_tree"]:
        print("=== ASCII-дерево ===")
        print(render_tree(params["package_name"], graph.get))
    write_png(graph, params["package_name"], params["graph_output"])
    print("image: " + params["graph_output"])
    return 0


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
    if params["test_repo_mode"] and os.path.isfile(params["repo_url"]):
        return run_test_graph(params)
    if not params["repo_url"].startswith("http"):
        print("[ERROR] этап 2 работает только с URL", file=sys.stderr)
        return 1
    try:
        deps = direct_dependencies(
            params["package_name"], params["package_version"],
            params["repo_url"],
        )
    except (OSError, ValueError, KeyError) as err:
        print(f"[ERROR] {err}", file=sys.stderr)
        return 1
    print("=== Прямые зависимости ===")
    for name in deps:
        print(name)
    return 0


def main():
    """Запуск с кодом выхода."""
    sys.exit(run())


if __name__ == "__main__":
    main()
