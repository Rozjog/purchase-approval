from django.http import HttpResponse

from homepage.views import page
from models.employees import find_employee_by_id
from storage import load_employees


EMPLOYEES_FILE = "data/employees.json"


def employees(request):
    employees_list = load_employees(
        EMPLOYEES_FILE
    )

    items = ""

    for employee in employees_list:
        items += f"""
        <li class="list-group-item">
            <a href="/employees/{employee.id}/">
                {employee.name} – {employee.role}
            </a>
        </li>
        """

    content = f"""
    <h1>Сотрудники</h1>

    <ul class="list-group">
        {items}
    </ul>
    """

    return HttpResponse(
        page(
            "Purchase Approval – сотрудники",
            content
        )
    )


def employee_detail(request, employee_id):
    employees_list = load_employees(
        EMPLOYEES_FILE
    )

    employee = find_employee_by_id(
        employees_list,
        employee_id
    )

    if employee is None:
        content = """
        <h1 class="text-danger">
            Сотрудник не найден
        </h1>

        <a href="/employees/"
           class="btn btn-outline-secondary">
            Назад к сотрудникам
        </a>
        """

        return HttpResponse(
            page(
                "Сотрудник не найден",
                content
            ),
            status=404
        )

    content = f"""
    <div class="card">
        <div class="card-body">

            <h5 class="card-title">
                {employee.name}
            </h5>

            <p>
                <strong>ID:</strong>
                {employee.id}
            </p>

            <p>
                <strong>Роль:</strong>
                {employee.role}
            </p>

            <a href="/employees/"
               class="btn btn-outline-secondary">
                Назад к сотрудникам
            </a>

        </div>
    </div>
    """

    return HttpResponse(
        page(
            employee.name,
            content
        ),
        status=200
    )
