from django.shortcuts import render
from db.database import get_connection

    
def requests(request):
    min_amount_text = request.GET.get("min_amount", "").strip()
    status = request.GET.get("status", "").strip()

    sql = """
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
        WHERE 1 = 1
    """

    parameters = []
    error = ""

    if min_amount_text:
        try:
            min_amount = int(min_amount_text)

            if min_amount < 0:
                raise ValueError

            sql += " AND requests.amount >= ?"
            parameters.append(min_amount)

        except ValueError:
            error = "Введите неотрицательную целую сумму."

    if status:
        sql += " AND requests.status = ?"
        parameters.append(status)

    sql += " ORDER BY requests.id"

    conn = get_connection()

    try:
        requests_list = conn.execute(
            sql,
            parameters
        ).fetchall()
    finally:
        conn.close()

    context = {
        "requests": requests_list,
        "min_amount": min_amount_text,
        "selected_status": status,
        "error": error,
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


def statistics(request):
    conn = get_connection()

    try:
        total_requests = conn.execute("""
            SELECT COUNT(*) AS requests_count
            FROM requests
        """).fetchone()["requests_count"]

        total_amount = conn.execute("""
            SELECT SUM(amount) AS total_amount
            FROM requests
        """).fetchone()["total_amount"] or 0

        request_statuses = conn.execute("""
            SELECT
                status,
                COUNT(*) AS requests_count
            FROM requests
            GROUP BY status
            ORDER BY requests_count DESC
        """).fetchall()

        approval_statuses = conn.execute("""
            SELECT
                status,
                COUNT(*) AS approvals_count
            FROM approvals
            GROUP BY status
            ORDER BY approvals_count DESC
        """).fetchall()

        popular_statuses = conn.execute("""
            SELECT
                status,
                COUNT(*) AS requests_count
            FROM requests
            GROUP BY status
            HAVING COUNT(*) >= 1
        """).fetchall()

    finally:
        conn.close()

    context = {
        "total_requests": total_requests,
        "total_amount": total_amount,
        "request_statuses": request_statuses,
        "approval_statuses": approval_statuses,
        "popular_statuses": popular_statuses,
    }

    return render(
        request,
        "purchase_requests/statistics.html",
        context,
    )
