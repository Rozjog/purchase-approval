import json

from models.employees import Employee
from models.requests import Request
from models.approvals import Approval
from models.decisions import Decision


def load_json(filename: str):
    try:
        with open(filename, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        return []


def save_json(filename: str, data: list):
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(
            data,
            file,
            ensure_ascii=False,
            indent=4
        )


def load_employees(filename: str):

    data = load_json(filename)
    employees = []

    for item in data:
        employee = Employee(
            item["id"],
            item["name"],
            item["role"]
        )

        employees.append(employee)

    return employees


def save_employees(filename: str, employees: list[Employee]):

    data = []

    for employee in employees:
        data.append({
            "id": employee.id,
            "name": employee.name,
            "role": employee.role
        })

    save_json(filename, data)


def load_requests(filename: str, employees: list[Employee]):

    data = load_json(filename)
    requests = []

    for item in data:
        employee = None

        for current_employee in employees:
            if current_employee.id == item["employee_id"]:
                employee = current_employee
                break

        if employee is None:
            continue

        request = Request(
            item["id"],
            item["name"],
            item["amount"],
            item["contractor"],
            employee
        )

        request.status = item.get(
            "status",
            "Создана"
        )

        requests.append(request)

    return requests


def save_requests(filename: str, requests: list[Request]):

    data = []

    for request in requests:
        data.append({
            "id": request.id,
            "name": request.name,
            "amount": request.amount,
            "contractor": request.contractor,
            "employee_id": request.employee.id,
            "status": request.status
        })

    save_json(filename, data)


def load_approvals(filename: str, requests: list[Request], employees: list[Employee]):
    data = load_json(filename)
    approvals = []

    for item in data:
        request = None
        employee = None

        for current_request in requests:
            if current_request.id == item["request_id"]:
                request = current_request
                break

        for current_employee in employees:
            if current_employee.id == item["employee_id"]:
                employee = current_employee
                break

        if request is None or employee is None:
            continue

        approval = Approval(
            item["id"],
            request,
            employee
        )

        approval.status = item.get(
            "status",
            "Ожидает решения"
        )

        approvals.append(approval)

    return approvals


def save_approvals(filename: str, approvals: list[Approval]):
    data = []

    for approval in approvals:
        data.append({
            "id": approval.id,
            "request_id": approval.request.id,
            "employee_id": approval.employee.id,
            "status": approval.status
        })

    save_json(filename, data)


def load_decisions(filename: str, approvals: list[Approval]):

    data = load_json(filename)
    decisions = []

    for item in data:
        approval = None

        for current_approval in approvals:
            if current_approval.id == item["approval_id"]:
                approval = current_approval
                break

        if approval is None:
            continue

        decision = Decision(
            item["id"],
            approval,
            item["result"],
            item["comment"]
        )

        decisions.append(decision)

    return decisions


def save_decisions(filename: str, decisions: list[Decision]):
    data = []

    for decision in decisions:
        data.append({
            "id": decision.id,
            "approval_id": decision.approval.id,
            "result": decision.result,
            "comment": decision.comment
        })

    save_json(filename, data)