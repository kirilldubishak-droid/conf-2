"""Сохранение изображения графа в формате PNG (этап 5).

Используются только struct и zlib из стандартной библиотеки.
Подписи рисуются встроенным шрифтом 5x7. Внешние программы
и библиотеки для картинок не требуются.
"""

import math
import struct
import zlib

from font5x7 import FONT
from place import layer_depths

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

SCALE = 2
GLYPH_W = 5
GLYPH_H = 7
PAD_X = 8
PAD_Y = 8
MARGIN = 20
ARROW_LEN = 10
ARROW_HALF = 0.5


class Canvas:
    """Прямоугольное поле пикселей."""

    def __init__(self, width, height):
        """Создать белое поле заданного размера."""
        self.width = width
        self.height = height
        self.rows = [[WHITE] * width for _ in range(height)]

    def px(self, x_pos, y_pos, color):
        """Поставить точку, если она внутри поля."""
        if 0 <= x_pos < self.width and 0 <= y_pos < self.height:
            self.rows[y_pos][x_pos] = color

    def fill(self, x_pos, y_pos, width, height, color):
        """Закрасить прямоугольник."""
        for row in range(y_pos, y_pos + height):
            for col in range(x_pos, x_pos + width):
                self.px(col, row, color)

    def line(self, x_from, y_from, x_to, y_to, color):
        """Отрезок алгоритмом Брезенхема."""
        diff_x = abs(x_to - x_from)
        diff_y = -abs(y_to - y_from)
        step_x = 1 if x_from < x_to else -1
        step_y = 1 if y_from < y_to else -1
        err = diff_x + diff_y
        x_pos, y_pos = x_from, y_from
        while True:
            self.px(x_pos, y_pos, color)
            if x_pos == x_to and y_pos == y_to:
                break
            double = 2 * err
            if double >= diff_y:
                err += diff_y
                x_pos += step_x
            if double <= diff_x:
                err += diff_x
                y_pos += step_y

    def frame(self, x_pos, y_pos, width, height):
        """Рамка прямоугольника толщиной 2."""
        self.fill(x_pos, y_pos, width, 2, BLACK)
        self.fill(x_pos, y_pos + height - 2, width, 2, BLACK)
        self.fill(x_pos, y_pos, 2, height, BLACK)
        self.fill(x_pos + width - 2, y_pos, 2, height, BLACK)

    def text(self, x_pos, y_pos, value):
        """Написать строку встроенным шрифтом."""
        for index, char in enumerate(value):
            glyph = FONT.get(char, FONT[" "])
            base_x = x_pos + index * (GLYPH_W + 1) * SCALE
            for row, bits in enumerate(glyph):
                for col, bit in enumerate(bits):
                    if bit == "1":
                        self.fill(base_x + col * SCALE,
                                  y_pos + row * SCALE,
                                  SCALE, SCALE, BLACK)

    def arrow(self, x_from, y_from, x_to, y_to):
        """Стрелка с наконечником."""
        self.line(x_from, y_from, x_to, y_to, BLACK)
        angle = math.atan2(y_to - y_from, x_to - x_from)
        for sign in (1, -1):
            wing = angle + sign * ARROW_HALF
            self.line(x_to, y_to,
                      int(x_to - ARROW_LEN * math.cos(wing)),
                      int(y_to - ARROW_LEN * math.sin(wing)),
                      BLACK)

    def to_png(self):
        """Собрать байты PNG: сигнатура, IHDR, IDAT, IEND."""
        body = b"".join(b"\x00" + b"".join(bytes(px) for px in row)
                        for row in self.rows)
        head = struct.pack(">IIBBBBB", self.width, self.height,
                           8, 2, 0, 0, 0)
        return (b"\x89PNG\r\n\x1a\n" + self.chunk(b"IHDR", head)
                + self.chunk(b"IDAT", zlib.compress(body))
                + self.chunk(b"IEND", b""))

    @staticmethod
    def chunk(tag, data):
        """Оформить чанк PNG с длиной и контрольной суммой."""
        block = tag + data
        return (struct.pack(">I", len(data)) + block
                + struct.pack(">I", zlib.crc32(block) & 0xffffffff))


def box_size(names):
    """Размер блока под самое длинное имя."""
    longest = max([len(n) for n in names] + [1])
    width = longest * (GLYPH_W + 1) * SCALE + PAD_X * 2
    return width, GLYPH_H * SCALE + PAD_Y * 2


def positions(graph, start, box_w, box_h):
    """Расставить блоки по слоям с отступами."""
    depth = layer_depths(graph, start)
    layers = {}
    for name, level in depth.items():
        layers.setdefault(level, []).append(name)
    x_step = box_w + 60
    y_step = box_h + 40
    pos = {}
    for level, names in layers.items():
        for index, name in enumerate(sorted(names)):
            pos[name] = (MARGIN + level * x_step,
                         MARGIN + index * y_step)
    return pos, x_step, y_step


def draw_graph(graph, start):
    """Нарисовать граф на холсте и вернуть его."""
    names = set(graph)
    for deps in graph.values():
        names.update(deps)
    box_w, box_h = box_size(names)
    pos, _, _ = positions(graph, start, box_w, box_h)
    max_x = max(x for x, _ in pos.values()) + box_w + MARGIN
    max_y = max(y for _, y in pos.values()) + box_h + MARGIN
    canvas = Canvas(max_x, max_y)
    for node, deps in sorted(graph.items()):
        if node not in pos:
            continue
        x_from, y_from = pos[node]
        for dep in deps:
            if dep not in pos:
                continue
            x_to, y_to = pos[dep]
            canvas.arrow(x_from + box_w, y_from + box_h // 2,
                         x_to, y_to + box_h // 2)
    for node, (x_box, y_box) in sorted(pos.items()):
        canvas.frame(x_box, y_box, box_w, box_h)
        canvas.text(x_box + PAD_X, y_box + PAD_Y, node)
    return canvas


def write_png(graph, start, path):
    """Сохранить изображение графа в PNG-файл."""
    with open(path, "wb") as handle:
        handle.write(draw_graph(graph, start).to_png())
