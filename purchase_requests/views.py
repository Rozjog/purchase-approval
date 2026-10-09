from django.http import HttpResponse
from homepage.views import page


def requests(request):
    content = """
    <h1>Заявки</h1>
    <p>Список заявок на закупку.</p>
    """

    return HttpResponse(
        page(
            "Purchase Approval – заявки",
            content
        )
    )


def request_detail(request, request_id):
    content = f"""
    <h1>Заявка {request_id}</h1>

    <a href="/requests/"
       class="btn btn-outline-secondary">
        Назад к заявкам
    </a>
    """

    return HttpResponse(
        page(
            f"Заявка {request_id}",
            content
        )
    )