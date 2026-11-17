"""Текстовое описание графа на языке Mermaid (этап 5)."""


def describe(graph):
    """Сформировать Mermaid-диаграмму: graph TD и стрелки."""
    lines = ["graph TD"]
    for node in sorted(graph):
        for dep in graph[node]:
            lines.append("    %s-->%s" % (node, dep))
    return "\n".join(lines)
