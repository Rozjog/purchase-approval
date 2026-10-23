from django.shortcuts import render
from db.database import get_connection


def decisions(request):
    conn = get_connection()

    try:
        decisions_list = conn.execute("""
            SELECT
                decisions.id,
                decisions.approval_id,
                decisions.result,
                decisions.comment,
                requests.name AS request_name,
                requests.amount AS request_amount
            FROM decisions
            JOIN approvals
                ON decisions.approval_id = approvals.id
            JOIN requests
                ON approvals.request_id = requests.id
            ORDER BY decisions.id
        """).fetchall()
    finally:
        conn.close()

    context = {
        "decisions": decisions_list,
    }

    return render(
        request,
        "decisions/decision_list.html",
        context,
    )


def decision_detail(request, decision_id):
    conn = get_connection()

    try:
        decision = conn.execute("""
            SELECT
                decisions.id,
                decisions.approval_id,
                decisions.result,
                decisions.comment,
                requests.name AS request_name,
                requests.amount AS request_amount
            FROM decisions
            JOIN approvals
                ON decisions.approval_id = approvals.id
            JOIN requests
                ON approvals.request_id = requests.id
            WHERE decisions.id = ?
        """, (decision_id,)).fetchone()
    finally:
        conn.close()

    context = {
        "decision": decision,
    }

    return render(
        request,
        "decisions/decision_detail.html",
        context,
        status=404 if decision is None else 200,
    )
