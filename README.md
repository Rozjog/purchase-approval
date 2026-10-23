# Purchase Approval — система согласования закупок

**Purchase Approval** — учебное приложение на Python и Django для учёта сотрудников, заявок на закупку, согласований и решений. Проект развивается последовательно: сначала была создана консольная версия с собственными Python-классами и JSON-хранилищем (ПР1–ПР3), затем веб-интерфейс на Django (ПР5), а в ПР6 страницы были переведены на систему Django Templates.

Веб-интерфейс на текущем этапе предназначен для **просмотра данных**. Создание и изменение объектов доступны в консольной версии; веб-формы и перенос предметных данных в Django ORM относятся к дальнейшим этапам.

## Возможности

- Просмотр списков сотрудников, заявок, согласований и решений.
- Просмотр подробной информации по каждому объекту.
- Отображение связанных данных: заявка и её автор, согласование и ответственный сотрудник, решение и соответствующая заявка.
- Отображение статусов согласований и обработка отсутствующих записей с кодом HTTP 404.
- Навигация с использованием именованных URL Django.
- Сохранение консольных операций из предыдущих практических работ: создание объектов, поиск, отмена заявок и принятие решений.
- Исходные данные предыдущих этапов сохранены в отдельных JSON-файлах; веб-интерфейс в ПР7 получает данные из SQLite.

## Технологии

- **Python 3** — язык программирования и реализация предметной области.
- **Django 5.2** — веб-фреймворк.
- **Django Template Language (DTL)** — наследование шаблонов, контекст, циклы, условия, фильтры и именованные ссылки.
- **HTML5, CSS3, JavaScript** — разметка, оформление и клиентское поведение.
- **Bootstrap 5.3** — готовые компоненты интерфейса.
- **JSON** — исходное хранилище сотрудников, заявок, согласований и решений.
- **SQLite и sqlite3** — реляционное хранение и выполнение SQL-запросов в ПР7.
- **pytest** — автоматизированные тесты.
- **flake8** — проверка оформления Python-кода.
- **Git** — контроль версий.

## Предметная область

В системе используются четыре взаимосвязанные сущности.

| Сущность | Класс | Основные поля | Назначение |
|---|---|---|---|
| Сотрудник | `Employee` | `id`, `name`, `role` | Информация о сотруднике и его роли |
| Заявка | `Request` | `id`, `name`, `amount`, `contractor`, `employee`, `status` | Запрос на закупку |
| Согласование | `Approval` | `id`, `request`, `employee`, `status` | Согласование заявки ответственным сотрудником |
| Решение | `Decision` | `id`, `approval`, `result`, `comment` | Результат рассмотрения согласования |

Классы находятся в отдельном пакете `models/` и не являются моделями Django ORM.

Основные методы предметной области:

- `Request.cancel()` — отмена заявки.
- `Approval.can_approve()` — проверка права на согласование в зависимости от роли сотрудника и суммы закупки: руководитель отдела может согласовать заявку на сумму до 250 000 рублей включительно, директор — на сумму свыше 250 000 рублей.
- `Decision.apply()` — применение результата решения к статусам согласования и связанной заявки.

## Страницы веб-интерфейса

| Адрес | Страница |
|---|---|
| `/` | Главная страница и навигация |
| `/employees/` | Список сотрудников |
| `/employees/<int:employee_id>/` | Информация о сотруднике |
| `/requests/` | Список заявок и поиск по сумме и статусу |
| `/requests/<int:request_id>/` | Информация о заявке |
| `/requests/statistics/` | Статистика заявок и согласований |
| `/approvals/` | Список согласований |
| `/approvals/<int:approval_id>/` | Информация о согласовании |
| `/decisions/` | Список решений |
| `/decisions/<int:decision_id>/` | Информация о решении |

Если запись с указанным идентификатором не найдена, соответствующее представление возвращает **HTTP 404**. Для несуществующих маршрутов предусмотрен отдельный обработчик `page_not_found()` с HTML-шаблоном `homepage/404.html`.

## Архитектура веб-части после ПР6

В ПР5 HTML-страницы формировались непосредственно в Python-коде через функцию `page()` и `HttpResponse`. В ПР6 HTML-разметка вынесена в отдельные шаблоны.

Последовательность обработки запроса в ПР7:

```text
HTTP-запрос
    ↓
URL-маршрут (urls.py)
    ↓
Представление (views.py)
    ↓
SQL-запрос к SQLite через db/database.py
    ↓
Контекст (context)
    ↓
render() → Django-шаблон (.html)
    ↓
Готовый HTML-ответ браузеру
```

Представления отвечают за получение и подготовку данных, а HTML-шаблоны — за их отображение. Функция `page()` больше не используется для формирования веб-страниц.

### Базовый шаблон и наследование

Общая структура сайта находится в `templates/base.html`: HTML-документ, подключение Bootstrap и собственных статических ресурсов, навигация, основной контейнер и подвал.

Дочерние страницы наследуют этот шаблон:

```django
{% extends "base.html" %}

{% block title %}Заявки — Purchase Approval{% endblock %}

{% block content %}
    <h1>Заявки на закупку</h1>
{% endblock %}
```

Используются блоки `title` и `content`, поэтому общий HTML-каркас не дублируется в каждом файле.

### Включаемые шаблоны

Повторяющиеся фрагменты вынесены в отдельные файлы:

- `templates/includes/navigation.html` — общее меню;
- `purchase_requests/templates/purchase_requests/includes/request_card.html` — карточка заявки;
- `approvals/templates/approvals/includes/approval_status.html` — оформление статуса согласования.

Подключение осуществляется тегом `{% include %}`. Например:

```django
{% include "purchase_requests/includes/request_card.html" %}
```

### Контекст, циклы и условия

Представления передают данные шаблонам через словарь `context`. Пример для списка заявок:

```python
context = {"requests": requests_list}
return render(request, "purchase_requests/request_list.html", context)
```

В шаблоне список перебирается с помощью `{% for %}`, а случай отсутствия записей обрабатывается через `{% empty %}`:

```django
{% for purchase_request in requests %}
    {% include "purchase_requests/includes/request_card.html" %}
{% empty %}
    <p>Заявок пока нет.</p>
{% endfor %}
```

Конструкция `{% if %}` используется, в частности, для проверки наличия объекта и отображения разных статусов согласования.

### Именованные URL и пространства имён

Для каждого Django-приложения задано `app_name`, а маршруты имеют имена `name`. Ссылки формируются с помощью `{% url %}`:

```django
{% url 'employees:employees' %}
{% url 'purchase_requests:requests' %}
{% url 'purchase_requests:request_detail' purchase_request.id %}
{% url 'approvals:approvals' %}
{% url 'decisions:decisions' %}
```

Это позволяет изменять адреса маршрутов без ручного исправления всех ссылок в шаблонах.

### Фильтры шаблонов

На странице заявок используются стандартные фильтры Django:

- `{{ requests|length }}` — количество заявок;
- `{{ purchase_request.name|default:"Без названия" }}` — запасное значение для пустого названия.

Фильтры влияют на отображение данных и не изменяют хранилище.

### Статические файлы

Собственные ресурсы находятся в `homepage/static/homepage/`:

| Файл | Назначение |
|---|---|
| `css/style.css` | Цвета, фон, оформление навигации, карточек и статусов |
| `img/logo.png` | Логотип проекта |
| `js/main.js` | Автоматический вывод текущего года в подвале сайта |

В `base.html` используется `{% load static %}`, а пути к файлам формируются через `{% static %}`. Для базовых элементов интерфейса дополнительно подключён Bootstrap 5.3.

## Хранение данных

Исходные данные предыдущих этапов сохранены в JSON-файлах:

```text
data/
├── employees.json
├── requests.json
├── approvals.json
└── decisions.json
```

Модуль `storage.py` загружает JSON и восстанавливает связи между Python-объектами по идентификаторам:

1. Сначала загружаются сотрудники `Employee`.
2. Затем заявки `Request` со ссылками на сотрудников.
3. Затем согласования `Approval`, связанные с заявками и сотрудниками.
4. Затем решения `Decision`, связанные с согласованиями.

В ПР6 **Django ORM для предметных сущностей не используется**. В ПР7 данные перенесены в отдельную базу `data/purchase_approval.sqlite`, из которой их получает веб-интерфейс через SQL и `sqlite3`; исходные JSON-файлы сохранены.

## Структура проекта

```text
purchase-approval/
├── README.md
├── requirements.txt
├── .flake8
├── .gitignore
├── manage.py
├── main.py
├── storage.py
├── utils.py
│
├── purchase_approval/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── templates/
│   ├── base.html
│   └── includes/
│       └── navigation.html
│
├── homepage/
│   ├── urls.py
│   ├── views.py
│   ├── templates/homepage/
│   │   ├── index.html
│   │   └── 404.html
│   └── static/homepage/
│       ├── css/style.css
│       ├── img/logo.png
│       └── js/main.js
│
├── employees/
│   ├── urls.py
│   ├── views.py
│   └── templates/employees/
│       ├── employee_list.html
│       └── employee_detail.html
│
├── purchase_requests/
│   ├── urls.py
│   ├── views.py
│   └── templates/purchase_requests/
│       ├── request_list.html
│       ├── request_detail.html
│       ├── statistics.html
│       └── includes/request_card.html
│
├── approvals/
│   ├── urls.py
│   ├── views.py
│   └── templates/approvals/
│       ├── approval_list.html
│       ├── approval_detail.html
│       └── includes/approval_status.html
│
├── decisions/
│   ├── urls.py
│   ├── views.py
│   └── templates/decisions/
│       ├── decision_list.html
│       └── decision_detail.html
│
├── models/
│   ├── employees.py
│   ├── requests.py
│   ├── approvals.py
│   └── decisions.py
│
├── db/
│   ├── __init__.py
│   ├── database.py
│   └── import_json.py
│
├── sql/
│   ├── schema.sql
│   └── queries.sql
│
├── data/
│   ├── purchase_approval.sqlite
│   ├── employees.json
│   ├── requests.json
│   ├── approvals.json
│   └── decisions.json
│
└── tests/
    ├── test_employees.py
    ├── test_requests.py
    ├── test_approvals.py
    └── test_decisions.py
```

*В дереве показаны основные файлы проекта; стандартные служебные файлы Django-приложений опущены.*

## Запуск проекта

В терминале Windows перейдите в корневую папку проекта и активируйте виртуальное окружение:

```powershell
venv\Scripts\activate
```

Установите зависимости (при необходимости):

```powershell
python -m pip install -r requirements.txt
```

При первом развёртывании создайте таблицы из `sql/schema.sql` и перенесите данные из JSON (подробности — в разделе «База данных SQLite (ПР7)» ниже).

Проверьте конфигурацию Django:

```powershell
python manage.py check
```

Запустите сервер разработки:

```powershell
python manage.py runserver
```

Откройте сайт: **http://127.0.0.1:8000/**

Для просмотра собственного CSS, изображения и JavaScript при использовании стандартного `runserver` включите `DEBUG = True` в локальных настройках. Режим отладки не предназначен для публичного развёртывания.

Консольная версия проекта по-прежнему доступна:

```powershell
python main.py
```

## Тестирование и проверка качества

Проверка конфигурации Django:

```powershell
python manage.py check
```

Запуск тестов предметной области:

```powershell
python -m pytest -v
```

Проверка Python-кода через flake8:

```powershell
python -m flake8 . --extend-exclude=venv
```

Для проверки поиска статических ресурсов:

```powershell
python manage.py findstatic homepage/css/style.css
python manage.py findstatic homepage/img/logo.png
python manage.py findstatic homepage/js/main.js
```

Также следует вручную проверить переходы между страницами, отображение пустых списков, различные статусы согласований и HTTP-статус 404 для несуществующих объектов и маршрутов.

## Работа с Git

Проект развивается в одном репозитории. Коммиты практической работы № 6 должны начинаться с префикса `PR6:`.

После успешной проверки изменений ПР7:

```powershell
git status
git add .
git commit -m "PR7: add SQLite database and SQL queries"
git push
```

## Текущее состояние и дальнейшее развитие

**Реализовано в ПР6:** шаблонная архитектура Django, базовый шаблон, наследование и блоки, подключаемые компоненты, контекст, циклы и условия, именованные URL, пространства имён, фильтры, собственные CSS/JavaScript/изображение и обработка 404. При этом сохранены классы предметной области, JSON-хранилище, консольная версия приложения и тесты предыдущих практических работ.

**Планируется:** переход к Django ORM, веб-формы для создания и изменения данных, авторизация и разграничение прав доступа, API, контейнеризация и CI/CD.

## База данных SQLite (ПР7)

В ПР7 предметные данные перенесены из JSON в SQLite. Django-представления получают записи с помощью SQL-запросов и стандартной библиотеки Python `sqlite3`, без использования Django ORM. JSON-файлы и консольная реализация сохранены.

### Структура таблиц и связи

База данных находится в `data/purchase_approval.sqlite`; команды создания таблиц — в `sql/schema.sql`.

| Таблица | Поля и типы данных | Ключи |
|---|---|---|
| `employees` | `id INTEGER`, `name TEXT`, `role TEXT` | `id` — PRIMARY KEY |
| `requests` | `id INTEGER`, `name TEXT`, `amount INTEGER`, `contractor TEXT`, `employee_id INTEGER`, `status TEXT` | `id` — PRIMARY KEY; `employee_id` → `employees.id` |
| `approvals` | `id INTEGER`, `request_id INTEGER`, `employee_id INTEGER`, `status TEXT` | `id` — PRIMARY KEY; `request_id` → `requests.id`, `employee_id` → `employees.id` |
| `decisions` | `id INTEGER`, `approval_id INTEGER`, `result TEXT`, `comment TEXT` | `id` — PRIMARY KEY; `approval_id` → `approvals.id` |

В `sql/schema.sql` таблицы создаются с помощью `CREATE TABLE IF NOT EXISTS`, а связи определяются внешними ключами `FOREIGN KEY`. В `db/database.py` настроено подключение к SQLite, проверка внешних ключей через `PRAGMA foreign_keys = ON` и получение именованных результатов через `sqlite3.Row`.

### Перенос данных из JSON

Скрипт `db/import_json.py` переносит записи из четырёх JSON-файлов в соответствующие таблицы с помощью `executemany()` и параметров `?`. Порядок импорта учитывает внешние ключи: сначала сотрудники, затем заявки, согласования и решения. Для сохранения изменений используется `commit()`, для отмены при ошибке — `rollback()`.

При первоначальном развёртывании из корня проекта:

```powershell
python -c "import sqlite3; c=sqlite3.connect('data/purchase_approval.sqlite'); c.executescript(open('sql/schema.sql', encoding='utf-8').read()); c.close()"
python -m db.import_json
```

Импорт выполняется **однократно**: при повторной вставке записей с теми же `id` возникнет конфликт первичных ключей.

### SQL-запросы

Все проверяемые SQL-команды сохранены в `sql/queries.sql`. В нём 16 запросов: списки сотрудников, заявок, согласований и решений; подробная информация по идентификатору; поиск заявок по сумме и статусу (`WHERE`); объединение связанных данных (`JOIN`); общее количество (`COUNT`) и сумма (`SUM`) заявок; группировка заявок и согласований по статусам (`GROUP BY`); пять самых дорогих заявок (`ORDER BY`, `LIMIT`, `OFFSET`); группировка с отбором по количеству (`HAVING`).

Примеры в `queries.sql` используют конкретные значения, а при передаче значений от пользователя Django выполняет **параметризованные запросы** с `?`.

### Использование SQL в Django

Представления приложений `employees`, `purchase_requests`, `approvals`, `decisions` выполняют SQL-запросы через `db/database.py`, получают записи с `fetchall()` или `fetchone()` и передают их в HTML-шаблоны через `context` и `render()`.

- `/employees/` — список сотрудников из SQLite.
- `/requests/` — список заявок и фильтрация по минимальной сумме и статусу через параметры GET.
- `/approvals/` — согласования с названиями заявок и именами ответственных (JOIN).
- `/decisions/` — решения со сведениями о связанных заявках (JOIN).
- `/requests/statistics/` — число и общая сумма заявок, распределение заявок и согласований по статусам, пять самых дорогих заявок.

Для проверки результатов используется файл `sql/queries.sql` и SQLite CLI; при наличии утилиты можно открыть базу командой `sqlite3 data/purchase_approval.sqlite` и выполнить `.read sql/queries.sql`.

Запрос с `HAVING` сохранён как отдельный учебный пример в `queries.sql`, **в статистике на сайте он не используется**.
