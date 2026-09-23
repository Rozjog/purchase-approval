from models.employees import Employee
from models.requests import Request
from models.approvals import (
    Approval,
    create_approval,
    find_approval_by_id
)


def test_create_approval() -> None:
    approvals: list = []

    employee = Employee(
        1,
        "Иван Иванов",
        "Директор"
    )

    request = Request(
        1,
        "Покупка оборудования",
        300000,
        "ООО Техно",
        employee
    )

    approval = create_approval(
        approvals,
        request,
        employee
    )

    assert len(approvals) == 1
    assert approval.id == 1
    assert approval.request is request
    assert approval.employee is employee
    assert approval.status == "Ожидает решения"


def test_can_approve() -> None:
    employee = Employee(
        1,
        "Иван Иванов",
        "Директор"
    )

    request = Request(
        1,
        "Покупка оборудования",
        300000,
        "ООО Техно",
        employee
    )

    approval = Approval(
        1,
        request,
        employee
    )

    assert approval.can_approve()


def test_find_approval_by_id() -> None:
    approvals: list = []

    employee = Employee(
        1,
        "Иван Иванов",
        "Директор"
    )

    request = Request(
        1,
        "Покупка оборудования",
        300000,
        "ООО Техно",
        employee
    )

    create_approval(
        approvals,
        request,
        employee
    )

    approval = find_approval_by_id(
        approvals,
        1
    )

    assert approval is not None
    assert approval.id == 1