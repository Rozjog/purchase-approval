from django.shortcuts import render
from db.database import get_connection


def employees(request):
    conn = get_connection()

    try:
        employees_list = conn.execute("""
            SELECT id, name, role
            FROM employees
            ORDER BY name
        """).fetchall()
    finally:
        conn.close()

    context = {
        "employees": employees_list,
    }

    return render(
        request,
        "employees/employee_list.html",
        context,
    )


def employee_detail(request, employee_id):
    conn = get_connection()

    try:
        employee = conn.execute("""
            SELECT id, name, role
            FROM employees
            WHERE id = ?
        """, (employee_id,)).fetchone()
    finally:
        conn.close()

    context = {
        "employee": employee,
    }

    return render(
        request,
        "employees/employee_detail.html",
        context,
        status=404 if employee is None else 200,
    )
