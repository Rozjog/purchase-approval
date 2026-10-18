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
- Хранение данных предметной области в отдельных JSON-файлах.

## Технологии

- **Python 3** — язык программирования и реализация предметной области.
- **Django 5.2** — веб-фреймворк.
- **Django Template Language (DTL)** — наследование шаблонов, контекст, циклы, условия, фильтры и именованные ссылки.
- **HTML5, CSS3, JavaScript** — разметка, оформление и клиентское поведение.
- **Bootstrap 5.3** — готовые компоненты интерфейса.
- **JSON** — хранение данных сотрудников, заявок, согласований и решений.
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
| `/requests/` | Список заявок |
| `/requests/<int:request_id>/` | Информация о заявке |
| `/approvals/` | Список согласований |
| `/approvals/<int:approval_id>/` | Информация о согласовании |
| `/decisions/` | Список решений |
| `/decisions/<int:decision_id>/` | Информация о решении |

Если запись с указанным идентификатором не найдена, соответствующее представление возвращает **HTTP 404**. Для несуществующих маршрутов предусмотрен отдельный обработчик `page_not_found()` с HTML-шаблоном `homepage/404.html`.

## Архитектура веб-части после ПР6

В ПР5 HTML-страницы формировались непосредственно в Python-коде через функцию `page()` и `HttpResponse`. В ПР6 HTML-разметка вынесена в отдельные шаблоны.

Текущая последовательность обработки запроса:

```text
HTTP-запрос
    ↓
URL-маршрут (urls.py)
    ↓
Представление (views.py)
    ↓
Загрузка объектов из JSON через storage.py
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

Фильтры влияют на отображение данных и не изменяют JSON-хранилище.

### Статические файлы

Собственные ресурсы находятся в `homepage/static/homepage/`:

| Файл | Назначение |
|---|---|
| `css/style.css` | Цвета, фон, оформление навигации, карточек и статусов |
| `img/logo.png` | Логотип проекта |
| `js/main.js` | Автоматический вывод текущего года в подвале сайта |

В `base.html` используется `{% load static %}`, а пути к файлам формируются через `{% static %}`. Для базовых элементов интерфейса дополнительно подключён Bootstrap 5.3.

## Хранение данных

Данные предметной области остаются в JSON-файлах:

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

В ПР6 **Django ORM для предметных сущностей не используется**. Стандартная конфигурация Django может содержать SQLite для встроенных компонентов фреймворка, но данные Purchase Approval продолжают храниться в JSON.

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
├── data/
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

После успешной проверки изменений:

```powershell
git status
git add .
git commit -m "PR6: add Django templates and static files"
git push
```

## Текущее состояние и дальнейшее развитие

**Реализовано в ПР6:** шаблонная архитектура Django, базовый шаблон, наследование и блоки, подключаемые компоненты, контекст, циклы и условия, именованные URL, пространства имён, фильтры, собственные CSS/JavaScript/изображение и обработка 404. При этом сохранены классы предметной области, JSON-хранилище, консольная версия приложения и тесты предыдущих практических работ.

**Планируется:** переход к базе данных и Django ORM, веб-формы для создания и изменения данных, авторизация и разграничение прав доступа, API, контейнеризация и CI/CD.
