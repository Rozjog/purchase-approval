from models.employees import Employee
from models.requests import Request
from models.approvals import Approval
from models.decisions import (
    Decision,
    create_decision,
    find_decision_by_id
)


def test_create_decision() -> None:
    decisions: list = []

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

    decision = create_decision(
        decisions,
        approval,
        "Согласована",
        "Закупка одобрена"
    )

    assert len(decisions) == 1
    assert decision.id == 1
    assert decision.approval is approval
    assert decision.result == "Согласована"


def test_apply_decision() -> None:
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

    decision = Decision(
        1,
        approval,
        "Согласована",
        "Закупка одобрена"
    )

    decision.apply()

    assert approval.status == "Согласована"
    assert request.status == "Согласована"


def test_find_decision_by_id() -> None:
    decisions: list = []

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

    create_decision(
        decisions,
        approval,
        "Согласована",
        "Закупка одобрена"
    )

    decision = find_decision_by_id(
        decisions,
        1
    )

    assert decision is not None
    assert decision.id == 1