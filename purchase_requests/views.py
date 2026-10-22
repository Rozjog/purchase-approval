from django.shortcuts import render
from models.requests import find_request_by_id
from storage import (
    load_employees,
    load_requests
)


EMPLOYEES_FILE = "data/employees.json"
REQUESTS_FILE = "data/requests.json"


def requests(request):
    employees_list = load_employees("data/employees.json")

    requests_list = load_requests(
        "data/requests.json",
        employees_list
    )

    context = {
        "requests": requests_list,
    }

    return render(
        request,
        "purchase_requests/request_list.html",
        context,
    )


def request_detail(request, request_id):
    employees_list = load_employees("data/employees.json")

    requests_list = load_requests(
        "data/requests.json",
        employees_list
    )

    purchase_request = find_request_by_id(
        requests_list,
        request_id
    )

    context = {
        "purchase_request": purchase_request,
    }

    return render(
        request,
        "purchase_requests/request_detail.html",
        context,
        status=404 if purchase_request is None else 200,
    )
