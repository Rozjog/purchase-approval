from django.shortcuts import render
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
    employees_list = load_employees("data/employees.json")

    requests_list = load_requests(
        "data/requests.json",
        employees_list
    )

    approvals_list = load_approvals(
        "data/approvals.json",
        requests_list,
        employees_list
    )

    context = {
        "approvals": approvals_list,
    }

    return render(
        request,
        "approvals/approval_list.html",
        context,
    )


def approval_detail(request, approval_id):
    employees_list = load_employees("data/employees.json")

    requests_list = load_requests(
        "data/requests.json",
        employees_list
    )

    approvals_list = load_approvals(
        "data/approvals.json",
        requests_list,
        employees_list
    )

    approval = find_approval_by_id(
        approvals_list,
        approval_id
    )

    context = {
        "approval": approval,
    }

    return render(
        request,
        "approvals/approval_detail.html",
        context,
        status=404 if approval is None else 200,
    )
