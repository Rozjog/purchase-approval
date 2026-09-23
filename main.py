from requests import (
    create_request,
    find_by_name,
    cancel_request,
    show_requests
)

from employees import (
    create_employee,
    find_employee_by_id,
    show_employees
)

from approvals import (
    create_approval,
    find_approval_by_id,
    show_approvals,
    approve_request
)

from decisions import (
    create_decision,
    show_decisions
)

from storage import load_data, save_data
from utils import input_int


REQUESTS_FILE = "data/requests.json"
EMPLOYEES_FILE = "data/employees.json"
APPROVALS_FILE = "data/approvals.json"
DECISIONS_FILE = "data/decisions.json"


def main() -> None:
    requests: list[dict] = load_data(REQUESTS_FILE)
    employees: list[dict] = load_data(EMPLOYEES_FILE)
    approvals: list[dict] = load_data(APPROVALS_FILE)
    decisions: list[dict] = load_data(DECISIONS_FILE)

    budget = 250000

    while True:
        print("\n=== Согласование закупок ===\n")
        print("1. Показать заявки")
        print("2. Создать заявку")
        print("3. Найти заявку")
        print("4. Отменить заявку")
        print("5. Показать сотрудников")
        print("6. Добавить сотрудника")
        print("7. Создать согласование")
        print("8. Показать согласования")
        print("9. Принять решение")
        print("10. Показать решения")
        print("0. Выход")

        choice = input_int("Выберите действие: ")

        if choice == 1:
            show_requests(requests)

        elif choice == 2:
            name = input("Название заявки: ")
            amount = input_int("Сумма: ")
            contractor = input("Контрагент: ")
            employee_id = input_int("ID сотрудника: ")

            employee = find_employee_by_id(
                employees,
                employee_id
            )

            if employee is None:
                print("Сотрудник не найден")
                continue

            create_request(
                requests,
                name,
                amount,
                contractor,
                employee_id
            )

            save_data(
                REQUESTS_FILE,
                requests
            )

            print("Заявка создана")

        elif choice == 3:
            name = input("Введите название заявки: ")

            request = find_by_name(
                requests,
                name
            )

            if request is None:
                print("Заявка не найдена")
            else:
                print(request)

        elif choice == 4:
            name = input("Введите название заявки: ")

            if cancel_request(requests, name):
                save_data(
                    REQUESTS_FILE,
                    requests
                )

                print("Заявка отменена")
            else:
                print("Заявка не найдена")

        elif choice == 5:
            show_employees(employees)

        elif choice == 6:
            name = input("Имя сотрудника: ")
            role = input("Роль сотрудника: ")

            create_employee(
                employees,
                name,
                role
            )

            save_data(
                EMPLOYEES_FILE,
                employees
            )

            print("Сотрудник добавлен")

        elif choice == 7:
            request_name = input(
                "Введите название заявки: "
            )

            request = find_by_name(
                requests,
                request_name
            )

            if request is None:
                print("Заявка не найдена")
                continue

            employee_id = input_int(
                "ID согласующего сотрудника: "
            )

            employee = find_employee_by_id(
                employees,
                employee_id
            )

            if employee is None:
                print("Сотрудник не найден")
                continue

            create_approval(
                approvals,
                request["id"],
                employee_id
            )

            save_data(
                APPROVALS_FILE,
                approvals
            )

            print("Согласование создано")

        elif choice == 8:
            show_approvals(approvals)

        elif choice == 9:
            approval_id = input_int(
                "ID согласования: "
            )

            approval = find_approval_by_id(
                approvals,
                approval_id
            )

            if approval is None:
                print("Согласование не найдено")
                continue

            employee = find_employee_by_id(
                employees,
                approval["employee_id"]
            )

            if employee is None:
                print("Сотрудник не найден")
                continue

            request = None

            for item in requests:
                if item["id"] == approval["request_id"]:
                    request = item
                    break

            if request is None:
                print("Заявка не найдена")
                continue

            budget = approve_request(
                request,
                budget,
                employee["role"]
            )

            approval["status"] = request["status"]

            comment = input(
                "Комментарий к решению: "
            )

            create_decision(
                decisions,
                approval["id"],
                request["status"],
                comment
            )

            save_data(
                REQUESTS_FILE,
                requests
            )

            save_data(
                APPROVALS_FILE,
                approvals
            )

            save_data(
                DECISIONS_FILE,
                decisions
            )

            print(
                "Решение:",
                request["status"]
            )

            print(
                "Остаток бюджета:",
                budget
            )

        elif choice == 10:
            show_decisions(decisions)

        elif choice == 0:
            save_data(
                REQUESTS_FILE,
                requests
            )

            save_data(
                EMPLOYEES_FILE,
                employees
            )

            save_data(
                APPROVALS_FILE,
                approvals
            )

            save_data(
                DECISIONS_FILE,
                decisions
            )

            print("Программа завершена")
            break

        else:
            print("Такого пункта нет")


if __name__ == "__main__":
    main()