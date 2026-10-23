from django.shortcuts import render
from db.database import get_connection


def approvals(request):
    conn = get_connection()

    try:
        approvals_list = conn.execute("""
            SELECT
                approvals.id,
                approvals.status,
                requests.name AS request_name,
                requests.amount AS request_amount,
                employees.name AS approver_name
            FROM approvals
            JOIN requests
                ON approvals.request_id = requests.id
            JOIN employees
                ON approvals.employee_id = employees.id
            ORDER BY approvals.id
        """).fetchall()
    finally:
        conn.close()

    context = {
        "approvals": approvals_list,
    }

    return render(
        request,
        "approvals/approval_list.html",
        context,
    )


def approval_detail(request, approval_id):
    conn = get_connection()

    try:
        approval = conn.execute("""
            SELECT
                approvals.id,
                approvals.status,
                requests.name AS request_name,
                requests.amount AS request_amount,
                employees.name AS approver_name
            FROM approvals
            JOIN requests
                ON approvals.request_id = requests.id
            JOIN employees
                ON approvals.employee_id = employees.id
            WHERE approvals.id = ?
        """, (approval_id,)).fetchone()
    finally:
        conn.close()

    context = {
        "approval": approval,
    }

    return render(
        request,
        "approvals/approval_detail.html",
        context,
        status=404 if approval is None else 200,
    )
