from django.http import HttpResponse

from homepage.views import page
from models.approvals import find_approval_by_id
from storage import (
    load_approvals,
    load_employees,
    load_requests
)


EMPLOYEES_FILE = "data/employees.json"
REQUESTS_FILE = "data/requests.json"
APPROVALS_FILE = "data/approvals.json"


def approvals(request):
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

    items = ""

    for approval in approvals_list:
        items += f"""
        <li class="list-group-item">
            <a href="/approvals/{approval.id}/">
                {approval.request.name}
                –
                {approval.employee.name}
                –
                {approval.status}
            </a>
        </li>
        """

    content = f"""
    <h1>Согласования</h1>

    <ul class="list-group">
        {items}
    </ul>
    """

    return HttpResponse(
        page(
            "Purchase Approval – согласования",
            content
        )
    )


def approval_detail(request, approval_id):
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

    approval = find_approval_by_id(
        approvals_list,
        approval_id
    )

    if approval is None:
        content = """
        <h1 class="text-danger">
            Согласование не найдено
        </h1>

        <a href="/approvals/"
           class="btn btn-outline-secondary">
            Назад к согласованиям
        </a>
        """

        return HttpResponse(
            page(
                "Согласование не найдено",
                content
            ),
            status=404
        )

    content = f"""
    <div class="card">
        <div class="card-body">

            <h5 class="card-title">
                Согласование №{approval.id}
            </h5>

            <p>
                <strong>Заявка:</strong>
                {approval.request.name}
            </p>

            <p>
                <strong>Сотрудник:</strong>
                {approval.employee.name}
            </p>

            <p>
                <strong>Роль:</strong>
                {approval.employee.role}
            </p>

            <p>
                <strong>Статус:</strong>
                {approval.status}
            </p>

            <a href="/approvals/"
               class="btn btn-outline-secondary">
                Назад к согласованиям
            </a>

        </div>
    </div>
    """

    return HttpResponse(
        page(
            f"Согласование №{approval.id}",
            content
        ),
        status=200
    )
