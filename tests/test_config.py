"""Тесты загрузки INI-конфига."""

import os
import sys

sys.path.insert(
    0,
    os.path.join(
        os.path.dirname(__file__), "..", "src"
    ),
)

from config_loader import load_config

ROOT = os.path.join(
    os.path.dirname(__file__), "..", "configs"
)


def test_ok():
    """Корректный конфиг."""
    path = os.path.join(ROOT, "config.ini")
    params = load_config(path)
    assert params["package_name"] == "serde"
    assert params["ascii_tree"] is True
    assert params["test_repo_mode"] is False


def test_missing_file():
    """Файл не найден."""
    try:
        load_config("/no/such/config.ini")
        assert False, "ожидался FileNotFoundError"
    except FileNotFoundError:
        pass


def test_empty_value():
    """Пустое значение."""
    path = os.path.join(ROOT, "bad_empty.ini")
    try:
        load_config(path)
        assert False, "ожидался ValueError"
    except ValueError as err:
        assert "пустой" in str(err)


def test_bad_bool():
    """Некорректный bool."""
    path = os.path.join(ROOT, "bad_bool.ini")
    try:
        load_config(path)
        assert False, "ожидался ValueError"
    except ValueError as err:
        assert "bool" in str(err).lower() or (
            "test_repo_mode" in str(err)
        )


def test_missing_keys():
    """Нет обязательных ключей."""
    path = os.path.join(ROOT, "bad_missing.ini")
    try:
        load_config(path)
        assert False, "ожидался ValueError"
    except ValueError as err:
        assert "обязательн" in str(err)


if __name__ == "__main__":
    test_ok()
    test_missing_file()
    test_empty_value()
    test_bad_bool()
    test_missing_keys()
    print("OK")
