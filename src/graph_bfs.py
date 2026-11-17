"""Построение графа зависимостей поиском в ширину (этап 3).

Тестовый репозиторий — текстовый файл, каждая строка вида
``ПАКЕТ: ЗАВИСИМОСТЬ1 ЗАВИСИМОСТЬ2``. Пустые строки и строки,
начинающиеся с `#`, пропускаются. Имена пакетов — большие
латинские буквы. Обход идёт без рекурсии, на явной очереди.
"""

from collections import deque

COMMENT_PREFIX = "#"
SEPARATOR = ":"


def load_test_repo(path):
    """Прочитать тестовый репозиторий в словарь пакет-список."""
    graph = {}
    with open(path, encoding="utf-8") as handle:
        for raw in handle:
            line = raw.strip()
            if not line or line.startswith(COMMENT_PREFIX):
                continue
            if SEPARATOR not in line:
                continue
            head, _, tail = line.partition(SEPARATOR)
            graph[head.strip()] = tail.split()
    return graph


def trace_cycle(parent, node, child):
    """Восстановить путь цикла от ребёнка через предков."""
    path = [child]
    current = node
    while current is not None and current != child:
        path.append(current)
        current = parent.get(current)
    path.append(child)
    path.reverse()
    return path


def is_ancestor(parent, node, target):
    """Проверить, что target — предок вершины node."""
    current = node
    while current is not None:
        if current == target:
            return True
        current = parent.get(current)
    return False


def bfs_iterative(start, get_deps, max_depth=0, skip=None):
    """Обход в ширину без рекурсии, с учётом глубины и циклов.

    Возвращает порядок обхода и найденные циклы (каждый цикл —
    список вершин, начинающийся и заканчивающийся одной вершиной).
    Глубина 0 означает отсутствие предела.
    """
    order = []
    cycles = []
    if skip is not None and skip(start):
        return order, cycles
    seen = {start}
    parent = {start: None}
    queue = deque([(start, 0)])
    order.append(start)

    def visit(child, node, depth):
        """Обработать потомка: в очередь или записать цикл."""
        if skip is not None and skip(child):
            return
        if child not in seen:
            seen.add(child)
            parent[child] = node
            order.append(child)
            queue.append((child, depth + 1))
        elif is_ancestor(parent, node, child):
            cycles.append(trace_cycle(parent, node, child))

    while queue:
        node, depth = queue.popleft()
        if max_depth and depth >= max_depth:
            continue
        for child in get_deps(node) or []:
            visit(child, node, depth)
    return order, cycles
