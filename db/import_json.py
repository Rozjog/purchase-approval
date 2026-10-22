
import json

from db.database import get_connection


def load_json(filename):
    with open(filename, encoding="utf-8") as file:
        return json.load(file)


def import_employees(conn):
    employees = load_json("data/employees.json")

    conn.executemany(
        """
        INSERT INTO employees (id, name, role)
        VALUES (?, ?, ?)
        """,
        [
            (item["id"], item["name"], item["role"])
            for item in employees
        ],
    )


def import_requests(conn):
    requests = load_json("data/requests.json")

    conn.executemany(
        """
        INSERT INTO requests (
            id, name, amount, contractor,
            employee_id, status
        )
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        [
            (
                item["id"],
                item["name"],
                item["amount"],
                item["contractor"],
                item["employee_id"],
                item.get("status", "Создана"),
            )
            for item in requests
        ],
    )


def import_approvals(conn):
    approvals = load_json("data/approvals.json")

    conn.executemany(
        """
        INSERT INTO approvals (
            id, request_id, employee_id, status
        )
        VALUES (?, ?, ?, ?)
        """,
        [
            (
                item["id"],
                item["request_id"],
                item["employee_id"],
                item.get("status", "Ожидает решения"),
            )
            for item in approvals
        ],
    )


def import_decisions(conn):
    decisions = load_json("data/decisions.json")

    conn.executemany(
        """
        INSERT INTO decisions (
            id, approval_id, result, comment
        )
        VALUES (?, ?, ?, ?)
        """,
        [
            (
                item["id"],
                item["approval_id"],
                item["result"],
                item["comment"],
            )
            for item in decisions
        ],
    )


def main():
    conn = get_connection()

    try:
        import_employees(conn)
        import_requests(conn)
        import_approvals(conn)
        import_decisions(conn)

        conn.commit()
        print("Данные успешно перенесены в SQLite.")

    except Exception:
        conn.rollback()
        raise

    finally:
        conn.close()


if __name__ == "__main__":
    main()
