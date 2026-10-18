from django.http import HttpResponse


def page(title, content):
    bootstrap = (
        "https://cdn.jsdelivr.net/npm/bootstrap@5.3.3"
        "/dist/css/bootstrap.min.css"
    )

    return f"""<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta
        name="viewport"
        content="width=device-width, initial-scale=1"
    >
    <title>{title}</title>
    <link rel="stylesheet" href="{bootstrap}">
</head>
<body>
    <nav class="nav">
        <a class="nav-link" href="/">Главная</a>
        <a class="nav-link" href="/employees/">Сотрудники</a>
        <a class="nav-link" href="/requests/">Заявки</a>
        <a class="nav-link" href="/approvals/">Согласования</a>
        <a class="nav-link" href="/decisions/">Решения</a>
    </nav>

    <main class="container">
        {content}
    </main>
</body>
</html>"""


def index(request):
    content = """
    <h1 class="display-4">Purchase Approval</h1>

    <p class="lead">
        Система согласования закупок.
    </p>

    <p>Основные разделы:</p>

    <a href="/employees/"
       class="btn btn-primary me-2">
        Сотрудники
    </a>

    <a href="/requests/"
       class="btn btn-secondary me-2">
        Заявки
    </a>

    <a href="/approvals/"
       class="btn btn-secondary me-2">
        Согласования
    </a>

    <a href="/decisions/"
       class="btn btn-secondary">
        Решения
    </a>
    """

    return HttpResponse(
        page("Purchase Approval2", content)
    )


def page_not_found(request, exception):
    content = """
    <h1 class="text-danger">404 – страница не найдена</h1>
    <p>Проверьте адрес или вернитесь на главную.</p>
    <a href="/" class="btn btn-primary">На главную</a>
    """

    return HttpResponse(
        page("404 – страница не найдена", content),
        status=404
    )
