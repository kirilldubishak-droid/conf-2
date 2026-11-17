"""Тесты порядка загрузки (этап 4)."""

import os
import sys

sys.path.insert(  # noqa: E402
    0,
    os.path.join(
        os.path.dirname(__file__), "..", "src"
    ),
)

from graph_bfs import (  # noqa: E402
    load_test_repo,
)
from order_topo import (  # noqa: E402
    load_order,
)

ROOT = os.path.join(
    os.path.dirname(__file__), "testdata"
)


def data(name):
    """Путь к файлу тестового репозитория."""
    return os.path.join(ROOT, name)


def getter(graph):
    """Зависимости вершины из словаря."""
    return lambda node: graph.get(node, [])


def test_chain():
    """Цепочка грузится с конца: C, B, A."""
    graph = load_test_repo(data("chain.txt"))
    assert load_order("A", getter(graph)) == ["C", "B", "A"]


def test_branch():
    """Общая зависимость первая, стартовая последняя."""
    graph = load_test_repo(data("branch.txt"))
    order = load_order("A", getter(graph))
    assert order[0] == "D"
    assert order[-1] == "A"
    assert sorted(order) == ["A", "B", "C", "D"]


def test_cycle_finishes():
    """Цикл не вешает программу, все вершины в порядке."""
    graph = load_test_repo(data("cycle.txt"))
    order = load_order("A", getter(graph))
    assert sorted(order) == ["A", "B", "C"]


if __name__ == "__main__":
    test_chain()
    test_branch()
    test_cycle_finishes()
    print("OK")
