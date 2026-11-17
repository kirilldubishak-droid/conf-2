"""Порядок загрузки зависимостей (этап 4).

Загрузка идёт снизу вверх: сначала пакеты без зависимостей,
затем те, чьи зависимости уже загружены. Циклы разрываются
по алфавиту, чтобы программа всегда завершалась.
"""

from graph_bfs import bfs_iterative


def pending_deps(node, get_deps, known, skip):
    """Незагруженные зависимости вершины с учётом фильтра."""
    result = set()
    for dep in get_deps(node) or []:
        if dep not in known:
            continue
        if skip is not None and skip(dep):
            continue
        result.add(dep)
    return result


def remaining_map(reached, get_deps, skip):
    """Словарь вершина-множество её незагруженных зависимостей."""
    known = set(reached)
    mapping = {}
    for node in reached:
        mapping[node] = pending_deps(node, get_deps, known, skip)
    return mapping


def load_order(start, get_deps, skip=None):
    """Вернуть порядок загрузки: зависимости раньше dependents."""
    reached, _ = bfs_iterative(start, get_deps, skip)
    remaining = remaining_map(reached, get_deps, skip)
    result = []
    while remaining:
        ready = sorted(n for n, ds in remaining.items() if not ds)
        if not ready:
            ready = sorted(remaining)
        for node in ready:
            result.append(node)
            del remaining[node]
        for deps in remaining.values():
            deps.difference_update(ready)
    return result
