"""Тесты прямых зависимостей Cargo (этап 2)."""

import json
import os
import sys

sys.path.insert(  # noqa: E402
    0,
    os.path.join(
        os.path.dirname(__file__), "..", "src"
    ),
)

from cargo_deps import (  # noqa: E402
    direct_dependencies,
    latest_version,
)

ROOT = os.path.join(
    os.path.dirname(__file__), "fixtures"
)


def load_fixture(name):
    """Прочитать JSON-приспособление."""
    path = os.path.join(ROOT, name)
    with open(path, encoding="utf-8") as handle:
        return json.load(handle)


def fake_opener(mapping):
    """Подменить сеть словарём адрес-ответ."""
    def opener(url):
        return mapping.get(url, {})
    return opener


def test_latest():
    """Отозванные версии пропускаются."""
    info = load_fixture("crate.json")
    assert latest_version(info) == "2.0.0"


def test_no_versions():
    """Без версий возвращается пусто."""
    assert latest_version({}) is None


def test_direct():
    """Сквозной разбор: пакет плюс зависимости."""
    info = load_fixture("crate.json")
    deps = load_fixture("deps.json")
    mapping = {
        "https://repo.example/api/crates/demo": info,
        "https://repo.example/api/crates/demo/2.0.0/"
        "dependencies": deps,
    }
    names = direct_dependencies(
        "demo", "2.0.0", "https://repo.example/api",
        fake_opener(mapping),
    )
    assert names == ["DepA", "DepB"]


def test_unknown_version():
    """Неизвестная версия даёт ошибку."""
    info = load_fixture("crate.json")
    try:
        direct_dependencies(
            "demo", "9.9.9", "https://repo.example/api",
            fake_opener({
                "https://repo.example/api/crates/demo": info
            }),
        )
        assert False, "ожидался ValueError"
    except ValueError as err:
        assert "версия" in str(err)


def test_dev_skipped():
    """Dev-зависимости и опциональные отсеиваются."""
    deps = load_fixture("deps.json")
    kinds = [d["kind"] for d in deps["dependencies"]]
    assert "dev" in kinds


if __name__ == "__main__":
    test_latest()
    test_no_versions()
    test_direct()
    test_unknown_version()
    test_dev_skipped()
    print("OK")
