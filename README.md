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

На **этапе 4** реализованы:

- вывод порядка загрузки зависимостей (сначала пакеты нижнего
  уровня, топологическая сортировка);
- сравнение со штатным менеджером (`cargo tree`): порядок уровней
  совпадает; возможные расхождения — в опциональных и dev-зависимостях,
  которые инструмент по заданию не учитывает.

На **этапе 5** реализованы:

- текстовое описание графа на языке диаграмм Mermaid (`graph TD`,
  стрелки `A-->B`);
- изображение графа в PNG-файле из параметра `graph_output`
  (прямоугольники по слоям, стрелки-рёбра, подписи встроенным
  шрифтом; внешние программы не требуются);
- ASCII-дерево, если задан параметр `ascii_tree = true`;
- примеры для трёх пакетов — ниже в разделе «Пример вывода»;
- сравнение со штатными средствами (`cargo tree -i`): состав рёбер
  совпадает, расхождения — только в оформлении.

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
python tests\test_order.py
python tests\test_visual.py
```

## Пример вывода

Тестовый режим (`python src/main.py --config configs/test_repo.ini`):

```
=== Параметры конфигурации ===
ascii_tree=True
graph_output=graph.png
package_name=A
package_version=1.0.0
repo_url=tests/testdata/cycle.txt
test_repo_mode=True
================================
=== Порядок обхода ===
A
B
C
=== Циклы ===
A -> B -> C -> A
=== Порядок загрузки ===
A
B
C
=== Mermaid ===
graph TD
    A-->B
    B-->C
    C-->A
=== ASCII-дерево ===
A
`-- B
    `-- C
        `-- A (повтор)
image: graph.png
```

Файл `graph.png` — картинка графа: прямоугольники-вершины
по слоям, стрелки-рёбра, подписи пакетов.

## Структура

```
├── README.md
├── .gitignore
├── run.bat / run.sh
├── src/
│   ├── main.py
│   ├── config_loader.py
│   ├── cargo_deps.py
│   ├── graph_bfs.py
│   ├── order_topo.py
│   ├── ascii_tree.py
│   ├── mermaid.py
│   ├── pngimg.py
│   └── font5x7.py
├── configs/
│   ├── config.ini
│   ├── test_repo.ini
│   └── bad_*.ini
└── tests/
    ├── test_config.py
    ├── test_cargo.py
    ├── test_graph.py
    ├── test_order.py
    ├── test_visual.py
    ├── testdata/
    └── fixtures/
```
