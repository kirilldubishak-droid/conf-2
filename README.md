# Граф зависимостей пакетов — Вариант 7

Практическая работа № 2. Конфигурационное управление.  
РТУ МИРЭА, 3 семестр 2026/2027.

## Общее описание

CLI-прототип инструмента визуализации графа зависимостей  
для менеджера пакетов (формат Cargo/Rust).

На **этапе 1** реализованы:

- чтение настроек из **INI**-файла;
- вывод всех параметров в формате `ключ=значение`;
- обработка ошибок для всех параметров.

На **этапе 2** реализованы:

- получение прямых зависимостей указанной версии пакета через API
  crates.io (только стандартная библиотека, без менеджеров пакетов);
- учитываются обычные, не опциональные зависимости;
- вывод прямых зависимостей на экран.

На **этапе 3** реализованы:

- чтение графа из тестового файла (строки вида `A: B C`, пакеты —
  большие латинские буквы) в режиме `test_repo_mode = true`;
- обход графа поиском в ширину без рекурсии (явная очередь);
- циклы находятся и выводятся, программа не зацикливается.

## Параметры конфигурации (`configs/config.ini`)

| Ключ | Описание |
|------|----------|
| `package_name` | имя анализируемого пакета |
| `repo_url` | URL репозитория или путь к тестовому файлу |
| `test_repo_mode` | режим тестового репозитория (`true`/`false`) |
| `package_version` | версия пакета |
| `graph_output` | имя файла с изображением графа |
| `ascii_tree` | вывод ASCII-дерева (`true`/`false`) |

Секция INI: `[app]`.

## Запуск

```bat
python src\main.py
python src\main.py --config configs\config.ini
run.bat
```

Примеры ошибок:

```bat
python src\main.py --config configs\bad_empty.ini
python src\main.py --config configs\bad_bool.ini
python src\main.py --config configs\bad_missing.ini
python src\main.py --config no_file.ini
```

## Тесты

```bat
python tests\test_config.py
python tests\test_cargo.py
python tests\test_graph.py
```

## Пример вывода

```
=== Параметры конфигурации ===
ascii_tree=True
graph_output=graph.svg
package_name=serde
package_version=1.0.210
repo_url=https://index.crates.io
test_repo_mode=False
================================
```

## Структура

```
├── README.md
├── .gitignore
├── run.bat / run.sh
├── src/
│   ├── main.py
│   └── config_loader.py
├── configs/
│   ├── config.ini
│   └── bad_*.ini
└── tests/
    └── test_config.py
```
