"""Слои вершин графа по расстоянию от старта (для диаграмм)."""

from collections import deque


def layer_depths(graph, start):
    """Уровень каждой вершины: расстояние поиском в ширину."""
    depth = {start: 0}
    queue = deque([start])
    while queue:
        node = queue.popleft()
        for child in graph.get(node) or []:
            if child not in depth:
                depth[child] = depth[node] + 1
                queue.append(child)
    names = set(graph)
    for deps in graph.values():
        names.update(deps)
    for name in sorted(names):
        if name not in depth:
            depth[name] = 0
    return depth


def layout(graph, start, x_step, y_step):
    """Позиции вершин: слои по горизонтали, порядок по вертикали."""
    depth = layer_depths(graph, start)
    layers = {}
    for name, level in depth.items():
        layers.setdefault(level, []).append(name)
    pos = {}
    for level, names in layers.items():
        for index, name in enumerate(sorted(names)):
            pos[name] = (level * x_step, index * y_step)
    return pos
