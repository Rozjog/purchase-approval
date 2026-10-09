from django.http import HttpResponse

from homepage.views import page
from models.requests import find_request_by_id
from storage import (
    load_employees,
    load_requests
)


EMPLOYEES_FILE = "data/employees.json"
REQUESTS_FILE = "data/requests.json"


def requests(request):
    employees_list = load_employees(
        EMPLOYEES_FILE
    )

    requests_list = load_requests(
        REQUESTS_FILE,
        employees_list
    )

    items = ""

    for item in requests_list:
        text = (
            f"{item.name} – "
            f"{item.amount} руб. – "
            f"{item.status}"
        )

        items += f"""
        <li class="list-group-item">
            <a href="/requests/{item.id}/">
                {text}
            </a>
        </li>
        """

    content = f"""
    <h1>Заявки</h1>

    <ul class="list-group">
        {items}
    </ul>
    """

    return HttpResponse(
        page(
            "Purchase Approval – заявки",
            content
        )
    )


def request_detail(request, request_id):
    employees_list = load_employees(
        EMPLOYEES_FILE
    )

    requests_list = load_requests(
        REQUESTS_FILE,
        employees_list
    )

    purchase_request = find_request_by_id(
        requests_list,
        request_id
    )

    if purchase_request is None:
        content = """
        <h1 class="text-danger">
            Заявка не найдена
        </h1>

        <a href="/requests/"
           class="btn btn-outline-secondary">
            Назад к заявкам
        </a>
        """

        return HttpResponse(
            page(
                "Заявка не найдена",
                content
            ),
            status=404
        )

    content = f"""
    <div class="card">
        <div class="card-body">

            <h5 class="card-title">
                {purchase_request.name}
            </h5>

            <p>
                <strong>ID:</strong>
                {purchase_request.id}
            </p>

            <p>
                <strong>Сумма:</strong>
                {purchase_request.amount} руб.
            </p>

            <p>
                <strong>Контрагент:</strong>
                {purchase_request.contractor}
            </p>

            <p>
                <strong>Сотрудник:</strong>
                {purchase_request.employee.name}
            </p>

            <p>
                <strong>Статус:</strong>
                {purchase_request.status}
            </p>

            <a href="/requests/"
               class="btn btn-outline-secondary">
                Назад к заявкам
            </a>

        </div>
    </div>
    """

    return HttpResponse(
        page(
            purchase_request.name,
            content
        ),
        status=200
    )
