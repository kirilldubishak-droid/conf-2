"""Прямые зависимости пакета Cargo (этап 2).

Только стандартная библиотека: urllib для HTTP, json для разбора.
Менеджеры пакетов и сторонние библиотеки не используются.
"""

import json
import urllib.request

HTTP_TIMEOUT = 20
CRATES_API_BASE = "https://crates.io/api/v1"
USER_AGENT = "conf-2/1.0 (student project)"


def fetch_json(url, opener=None):
    """Скачать JSON по адресу и разобрать в словарь."""
    if opener is not None:
        return opener(url)
    request = urllib.request.Request(
        url, headers={"User-Agent": USER_AGENT}
    )
    with urllib.request.urlopen(request, timeout=HTTP_TIMEOUT) as resp:
        return json.loads(resp.read().decode("utf-8"))


def latest_version(info):
    """Выбрать свежую не отозванную версию пакета."""
    for version in info.get("versions", []):
        if not version.get("yanked"):
            return version.get("num")
    return None


def known_versions(info):
    """Все известные версии пакета списком."""
    return [
        v.get("num") for v in info.get("versions", []) if v.get("num")
    ]


def direct_dependencies(package, version, repo_base=None, opener=None):
    """Прямые зависимости указанной версии пакета.

    Учитываются обычные (не dev, не сборка) и не опциональные
    зависимости: именно они нужны пакету всегда.
    """
    base = (repo_base or CRATES_API_BASE).rstrip("/")
    info = fetch_json(f"{base}/crates/{package}", opener)
    if version not in known_versions(info):
        raise ValueError(f"версия не найдена: {version}")
    url = f"{base}/crates/{package}/{version}/dependencies"
    answer = fetch_json(url, opener)
    names = []
    for dep in answer.get("dependencies", []):
        if dep.get("kind") != "normal" or dep.get("optional"):
            continue
        crate_id = dep.get("crate_id")
        if crate_id and crate_id not in names:
            names.append(crate_id)
    return names
