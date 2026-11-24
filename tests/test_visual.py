"""Тесты Mermaid-описания и PNG-картинки (этап 5)."""

import os
import sys

sys.path.insert(              
    0,
    os.path.join(
        os.path.dirname(__file__), "..", "src"
    ),
)

from graph_bfs import (              
    load_test_repo,
)
from mermaid import (              
    describe,
)
from pngimg import (              
    write_png,
)

MIN_PNG_SIZE = 500


ROOT = os.path.join(
    os.path.dirname(__file__), "testdata"
)
HERE = os.path.dirname(os.path.abspath(__file__))


def data(name):
    """Путь к файлу тестового репозитория."""
    return os.path.join(ROOT, name)


def test_frame():
    """Описание начинается с graph TD."""
    graph = load_test_repo(data("chain.txt"))
    assert describe(graph).startswith("graph TD")


def test_edges():
    """Все рёбра присутствуют в виде стрелок."""
    graph = load_test_repo(data("branch.txt"))
    text = describe(graph)
    assert "A-->B" in text
    assert "A-->C" in text
    assert "B-->D" in text
    assert "C-->D" in text


def test_signature():
    """Файл начинается с сигнатуры PNG."""
    path = os.path.join(HERE, "tmp_graph.png")
    try:
        graph = load_test_repo(data("branch.txt"))
        write_png(graph, "A", path)
        with open(path, "rb") as handle:
            head = handle.read(8)
        assert head == b"\x89PNG\r\n\x1a\n"
    finally:
        if os.path.exists(path):
            os.remove(path)


def test_size():
    """Картинка не пустая и имеет разумный размер."""
    path = os.path.join(HERE, "tmp_graph.png")
    try:
        graph = load_test_repo(data("chain.txt"))
        write_png(graph, "A", path)
        assert os.path.getsize(path) > MIN_PNG_SIZE
    finally:
        if os.path.exists(path):
            os.remove(path)


if __name__ == "__main__":
    test_frame()
    test_edges()
    test_signature()
    test_size()
    print("OK")
