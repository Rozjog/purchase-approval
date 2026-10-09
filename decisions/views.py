from django.http import HttpResponse

from homepage.views import page
from models.decisions import find_decision_by_id
from storage import (
    load_approvals,
    load_decisions,
    load_employees,
    load_requests
)


EMPLOYEES_FILE = "data/employees.json"
REQUESTS_FILE = "data/requests.json"
APPROVALS_FILE = "data/approvals.json"
DECISIONS_FILE = "data/decisions.json"


def decisions(request):
    employees_list = load_employees(
        EMPLOYEES_FILE
    )

    requests_list = load_requests(
        REQUESTS_FILE,
        employees_list
    )

    approvals_list = load_approvals(
        APPROVALS_FILE,
        requests_list,
        employees_list
    )

    decisions_list = load_decisions(
        DECISIONS_FILE,
        approvals_list
    )

    items = ""

    for decision in decisions_list:
        items += f"""
        <li class="list-group-item">
            <a href="/decisions/{decision.id}/">
                Решение №{decision.id}
                –
                {decision.result}
            </a>
        </li>
        """

    content = f"""
    <h1>Решения</h1>

    <ul class="list-group">
        {items}
    </ul>
    """

    return HttpResponse(
        page(
            "Purchase Approval – решения",
            content
        )
    )


def decision_detail(request, decision_id):
    employees_list = load_employees(
        EMPLOYEES_FILE
    )

    requests_list = load_requests(
        REQUESTS_FILE,
        employees_list
    )

    approvals_list = load_approvals(
        APPROVALS_FILE,
        requests_list,
        employees_list
    )

    decisions_list = load_decisions(
        DECISIONS_FILE,
        approvals_list
    )

    decision = find_decision_by_id(
        decisions_list,
        decision_id
    )

    if decision is None:
        content = """
        <h1 class="text-danger">
            Решение не найдено
        </h1>

        <a href="/decisions/"
           class="btn btn-outline-secondary">
            Назад к решениям
        </a>
        """

        return HttpResponse(
            page(
                "Решение не найдено",
                content
            ),
            status=404
        )

    content = f"""
    <div class="card">
        <div class="card-body">

            <h5 class="card-title">
                Решение №{decision.id}
            </h5>

            <p>
                <strong>Согласование:</strong>
                №{decision.approval.id}
            </p>

            <p>
                <strong>Заявка:</strong>
                {decision.approval.request.name}
            </p>

            <p>
                <strong>Результат:</strong>
                {decision.result}
            </p>

            <p>
                <strong>Комментарий:</strong>
                {decision.comment}
            </p>

            <a href="/decisions/"
               class="btn btn-outline-secondary">
                Назад к решениям
            </a>

        </div>
    </div>
    """

    return HttpResponse(
        page(
            f"Решение №{decision.id}",
            content
        ),
        status=200
    )
