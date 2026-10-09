from django.http import HttpResponse

from homepage.views import page


def decisions(request):
    content = """
    <h1>Решения</h1>
    <p>Список решений по согласованиям.</p>
    """

    return HttpResponse(
        page(
            "Purchase Approval – решения",
            content
        )
    )


def decision_detail(request, decision_id):
    content = f"""
    <h1>Решение {decision_id}</h1>

    <a href="/decisions/"
       class="btn btn-outline-secondary">
        Назад к решениям
    </a>
    """

    return HttpResponse(
        page(
            f"Решение {decision_id}",
            content
        )
    )