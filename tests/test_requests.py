from models.employees import Employee
from models.requests import (
    create_request,
    find_by_name,
    cancel_request
)


def test_create_request() -> None:
    requests: list = []

    employee = Employee(
        1,
        "Иван Иванов",
        "Сотрудник"
    )

    request = create_request(
        requests,
        "Покупка ноутбуков",
        180000,
        "ООО Техно",
        employee
    )

    assert len(requests) == 1
    assert request.id == 1
    assert request.name == "Покупка ноутбуков"
    assert request.amount == 180000
    assert request.employee.name == "Иван Иванов"
    assert request.status == "Создана"


def test_find_by_name() -> None:
    requests: list = []

    employee = Employee(
        1,
        "Иван Иванов",
        "Сотрудник"
    )

    create_request(
        requests,
        "Покупка ноутбуков",
        180000,
        "ООО Техно",
        employee
    )

    request = find_by_name(
        requests,
        "ноутбуков"
    )

    assert request is not None
    assert request.name == "Покупка ноутбуков"


def test_cancel_request() -> None:
    requests: list = []

    employee = Employee(
        1,
        "Иван Иванов",
        "Сотрудник"
    )

    create_request(
        requests,
        "Покупка ноутбуков",
        180000,
        "ООО Техно",
        employee
    )

    result = cancel_request(
        requests,
        "ноутбуков"
    )

    assert result
    assert requests[0].status == "Отменена"