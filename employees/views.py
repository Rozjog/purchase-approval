from django.http import HttpResponse
from homepage.views import page


def employees(request):
    content = """
    <h1>Сотрудники</h1>
    <p>Список сотрудников системы.</p>
    """

    return HttpResponse(
        page(
            "Purchase Approval – сотрудники",
            content
        )
    )


def employee_detail(request, employee_id):
    content = f"""
    <h1>Сотрудник {employee_id}</h1>

    <a href="/employees/"
       class="btn btn-outline-secondary">
        Назад к сотрудникам
    </a>
    """

    return HttpResponse(
        page(
            f"Сотрудник {employee_id}",
            content
        )
    )