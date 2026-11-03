
import os
import sqlite3
import sys
from contextlib import closing
from pathlib import Path

import django
from django.db import transaction


BASE_DIR = Path(__file__).resolve().parent.parent
SOURCE_DB = BASE_DIR / "data" / "purchase_approval.sqlite"


def main():
    # Подключаем настройки нашего Django-проекта.
    sys.path.insert(0, str(BASE_DIR))
    os.environ.setdefault(
        "DJANGO_SETTINGS_MODULE",
        "purchase_approval.settings",
    )
    django.setup()

    from employees.models import Employee
    from purchase_requests.models import Request
    from approvals.models import Approval
    from decisions.models import Decision

    if not SOURCE_DB.exists():
        raise FileNotFoundError(
            f"Исходная база не найдена: {SOURCE_DB}"
        )

    # Считываем данные из старой базы ПР7.
    with closing(sqlite3.connect(SOURCE_DB)) as source:
        source.row_factory = sqlite3.Row

        employees = source.execute("""
            SELECT id, name, role
            FROM employees
            ORDER BY id
        """).fetchall()

        requests = source.execute("""
            SELECT
                id, name, amount, contractor,
                employee_id, status
            FROM requests
            ORDER BY id
        """).fetchall()

        approvals = source.execute("""
            SELECT id, request_id, employee_id, status
            FROM approvals
            ORDER BY id
        """).fetchall()

        decisions = source.execute("""
            SELECT id, approval_id, result, comment
            FROM decisions
            ORDER BY id
        """).fetchall()

    # Переносим записи в базу Django одной транзакцией.
    with transaction.atomic():

        # 1. Сотрудники
        for row in employees:
            Employee.objects.update_or_create(
                pk=row["id"],
                defaults={
                    "name": row["name"],
                    "role": row["role"],
                },
            )

        # 2. Заявки
        for row in requests:
            Request.objects.update_or_create(
                pk=row["id"],
                defaults={
                    "name": row["name"],
                    "amount": row["amount"],
                    "contractor": row["contractor"],
                    "employee_id": row["employee_id"],
                    "status": row["status"],
                },
            )

        # 3. Согласования
        for row in approvals:
            Approval.objects.update_or_create(
                pk=row["id"],
                defaults={
                    "request_id": row["request_id"],
                    "employee_id": row["employee_id"],
                    "status": row["status"],
                },
            )

        # 4. Решения
        for row in decisions:
            Decision.objects.update_or_create(
                pk=row["id"],
                defaults={
                    "approval_id": row["approval_id"],
                    "result": row["result"],
                    "comment": row["comment"],
                },
            )

    print("Перенос данных завершён.")
    print(f"Сотрудников: {Employee.objects.count()}")
    print(f"Заявок: {Request.objects.count()}")
    print(f"Согласований: {Approval.objects.count()}")
    print(f"Решений: {Decision.objects.count()}")


if __name__ == "__main__":
    main()
