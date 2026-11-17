"""Вывод зависимостей в формате ASCII-дерева (этап 4)."""

T_BRANCH = "+-- "
T_LAST = "`-- "
T_PIPE = "|   "
T_GAP = "    "
T_REPEAT = " (повтор)"


def render_children(node, get_deps, prefix, max_depth, depth,
                    seen, lines):
    """Добавить в список строки-потомки вершины с префиксами."""
    children = list(get_deps(node) or [])
    for pos, child in enumerate(children):
        if pos == len(children) - 1:
            head, tail = T_LAST, T_GAP
        else:
            head, tail = T_BRANCH, T_PIPE
        if child in seen:
            lines.append(prefix + head + child + T_REPEAT)
            continue
        lines.append(prefix + head + child)
        if max_depth and depth >= max_depth:
            continue
        seen.add(child)
        render_children(child, get_deps, prefix + tail,
                        max_depth, depth + 1, seen, lines)


def render_tree(start, get_deps, max_depth=0):
    """Построить ASCII-дерево зависимостей от стартового пакета."""
    lines = [start]
    render_children(start, get_deps, "", max_depth, 1, {start},
                    lines)
    return "\n".join(lines)
