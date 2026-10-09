from django.http import HttpResponse
from homepage.views import page


def approvals(request):
    content = """
    <h1>Согласования</h1>
    <p>Список согласований заявок.</p>
    """

    return HttpResponse(
        page(
            "Purchase Approval – согласования",
            content
        )
    )


def approval_detail(request, approval_id):
    content = f"""
    <h1>Согласование {approval_id}</h1>

    <a href="/approvals/"
       class="btn btn-outline-secondary">
        Назад к согласованиям
    </a>
    """

    return HttpResponse(
        page(
            f"Согласование {approval_id}",
            content
        )
    )