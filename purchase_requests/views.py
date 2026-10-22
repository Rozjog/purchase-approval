from django.shortcuts import render
from db.database import get_connection


def requests(request):
    conn = get_connection()

    try:
        requests_list = conn.execute("""
            SELECT
                requests.id,
                requests.name,
                requests.amount,
                requests.contractor,
                requests.status,
                employees.name AS employee_name
            FROM requests
            JOIN employees
                ON requests.employee_id = employees.id
            ORDER BY requests.id
        """).fetchall()
    finally:
        conn.close()

    context = {
        "requests": requests_list,
    }

    return render(
        request,
        "purchase_requests/request_list.html",
        context,
    )


def request_detail(request, request_id):
    conn = get_connection()

    try:
        purchase_request = conn.execute("""
            SELECT
                requests.id,
                requests.name,
                requests.amount,
                requests.contractor,
                requests.status,
                employees.name AS employee_name
            FROM requests
            JOIN employees
                ON requests.employee_id = employees.id
            WHERE requests.id = ?
        """, (request_id,)).fetchone()
    finally:
        conn.close()

    context = {
        "purchase_request": purchase_request,
    }

    return render(
        request,
        "purchase_requests/request_detail.html",
        context,
        status=404 if purchase_request is None else 200,
    )
