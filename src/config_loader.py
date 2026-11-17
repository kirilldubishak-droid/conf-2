"""Загрузка и проверка INI-конфигурации."""

import configparser
import os

# обязательные ключи секции [app]
REQUIRED = (
    "package_name",
    "repo_url",
    "test_repo_mode",
    "package_version",
    "graph_output",
    "ascii_tree",
)

BOOL_KEYS = ("test_repo_mode", "ascii_tree")


def load_ini(path):
    """Читает INI-файл. Возвращает ConfigParser."""
    if not path:
        raise ValueError("не указан путь к конфигу")
    if not os.path.isfile(path):
        raise FileNotFoundError(
            f"конфиг не найден: {path}"
        )
    parser = configparser.ConfigParser()
    try:
        read = parser.read(path, encoding="utf-8")
    except configparser.Error as err:
        raise ValueError(f"ошибка INI: {err}") from err
    if not read:
        raise ValueError(
            f"не удалось прочитать: {path}"
        )
    return parser


def get_section(parser):
    """Возвращает секцию [app] или первую."""
    if parser.has_section("app"):
        return "app"
    sections = parser.sections()
    if not sections:
        raise ValueError("в INI нет секций")
    return sections[0]


def parse_bool(raw, key):
    """Строка -> bool для флагов."""
    val = raw.strip().lower()
    if val in ("1", "true", "yes", "on"):
        return True
    if val in ("0", "false", "no", "off"):
        return False
    raise ValueError(
        f"параметр '{key}': ожидался bool, "
        f"получено '{raw}'"
    )


def validate_params(raw):
    """Проверяет словарь параметров."""
    missing = [k for k in REQUIRED if k not in raw]
    if missing:
        names = ", ".join(missing)
        raise ValueError(
            f"нет обязательных ключей: {names}"
        )
    result = {}
    for key in REQUIRED:
        value = raw[key].strip()
        if not value:
            raise ValueError(
                f"параметр '{key}' пустой"
            )
        if key in BOOL_KEYS:
            result[key] = parse_bool(value, key)
        else:
            result[key] = value
    return result


def load_config(path):
    """Загружает и проверяет конфиг. Dict."""
    parser = load_ini(path)
    section = get_section(parser)
    raw = dict(parser.items(section))
    return validate_params(raw)
