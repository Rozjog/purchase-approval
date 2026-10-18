from django.shortcuts import render
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
        "data/employees.json"
    )

    requests_list = load_requests(
        "data/requests.json",
        employees_list
    )

    approvals_list = load_approvals(
        "data/approvals.json",
        requests_list,
        employees_list
    )

    decisions_list = load_decisions(
        "data/decisions.json",
        approvals_list
    )

    context = {
        "decisions": decisions_list,
    }

    return render(
        request,
        "decisions/decision_list.html",
        context,
    )



def decision_detail(request, decision_id):
    employees_list = load_employees(
        "data/employees.json"
    )

    requests_list = load_requests(
        "data/requests.json",
        employees_list
    )

    approvals_list = load_approvals(
        "data/approvals.json",
        requests_list,
        employees_list
    )

    decisions_list = load_decisions(
        "data/decisions.json",
        approvals_list
    )

    decision = find_decision_by_id(
        decisions_list,
        decision_id
    )

    context = {
        "decision": decision,
    }

    return render(
        request,
        "decisions/decision_detail.html",
        context,
        status=404 if decision is None else 200,
    )
