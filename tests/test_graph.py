"""Тесты обхода графа поиском в ширину (этап 3)."""

import os
import sys

sys.path.insert(              
    0,
    os.path.join(
        os.path.dirname(__file__), "..", "src"
    ),
)

from graph_bfs import (              
    bfs_iterative,
    load_test_repo,
    trace_cycle,
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


def test_load():
    """Файл читается в словарь смежности."""
    graph = load_test_repo(data("chain.txt"))
    assert graph == {"A": ["B"], "B": ["C"], "C": []}


def test_chain_order():
    """Линейная цепочка обходится по порядку."""
    graph = load_test_repo(data("chain.txt"))
    order, cycles = bfs_iterative("A", getter(graph))
    assert order == ["A", "B", "C"]
    assert cycles == []


def test_branch_level():
    """Ветвление обходится по уровням."""
    graph = load_test_repo(data("branch.txt"))
    order, cycles = bfs_iterative("A", getter(graph))
    assert order == ["A", "B", "C", "D"]
    assert cycles == []


def test_depth_limit():
    """Глубина ограничивает обход."""
    graph = load_test_repo(data("branch.txt"))
    order, _ = bfs_iterative("A", getter(graph), max_depth=1)
    assert order == ["A", "B", "C"]


def test_cycle_found():
    """Цикл находится и обход завершается."""
    graph = load_test_repo(data("cycle.txt"))
    order, cycles = bfs_iterative("A", getter(graph))
    assert sorted(order) == ["A", "B", "C"]
    assert len(cycles) == 1
    assert cycles[0][0] == cycles[0][-1]


def test_trace():
    """Путь цикла восстанавливается по предкам."""
    parent = {"A": None, "B": "A", "C": "B"}
    assert trace_cycle(parent, "C", "A") == ["A", "B", "C", "A"]


if __name__ == "__main__":
    test_load()
    test_chain_order()
    test_branch_level()
    test_depth_limit()
    test_cycle_found()
    test_trace()
    print("OK")
