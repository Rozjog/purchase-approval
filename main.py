from models.requests import (
    create_request,
    find_by_name,
    cancel_request,
    show_requests
)

from models.employees import (
    create_employee,
    find_employee_by_id,
    show_employees
)

from models.approvals import (
    create_approval,
    find_approval_by_id,
    show_approvals
)

from models.decisions import (
    create_decision,
    show_decisions
)

from storage import (
    load_employees,
    load_requests,
    load_approvals,
    load_decisions,
    save_employees,
    save_requests,
    save_approvals,
    save_decisions
)

from utils import input_int


REQUESTS_FILE = "data/requests.json"
EMPLOYEES_FILE = "data/employees.json"
APPROVALS_FILE = "data/approvals.json"
DECISIONS_FILE = "data/decisions.json"


def main() -> None:
    employees = load_employees(
        EMPLOYEES_FILE
    )

    requests = load_requests(
        REQUESTS_FILE,
        employees
    )

    approvals = load_approvals(
        APPROVALS_FILE,
        requests,
        employees
    )

    decisions = load_decisions(
        DECISIONS_FILE,
        approvals
    )

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

        choice = input_int(
            "Выберите действие: "
        )

        if choice == 1:
            show_requests(requests)

        elif choice == 2:
            name = input(
                "Название заявки: "
            )

            amount = input_int(
                "Сумма: "
            )

            contractor = input(
                "Контрагент: "
            )

            employee_id = input_int(
                "ID сотрудника: "
            )

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
                employee
            )

            save_requests(
                REQUESTS_FILE,
                requests
            )

            print("Заявка создана")

        elif choice == 3:
            name = input(
                "Введите название заявки: "
            )

            request = find_by_name(
                requests,
                name
            )

            if request is None:
                print("Заявка не найдена")
            else:
                print(request)

        elif choice == 4:
            name = input(
                "Введите название заявки: "
            )

            if cancel_request(
                requests,
                name
            ):
                save_requests(
                    REQUESTS_FILE,
                    requests
                )

                print("Заявка отменена")
            else:
                print("Заявка не найдена")

        elif choice == 5:
            show_employees(employees)

        elif choice == 6:
            name = input(
                "Имя сотрудника: "
            )

            role = input(
                "Роль сотрудника: "
            )

            create_employee(
                employees,
                name,
                role
            )

            save_employees(
                EMPLOYEES_FILE,
                employees
            )

            print("Сотрудник добавлен")

        elif choice == 7:
            name = input(
                "Введите название заявки: "
            )

            request = find_by_name(
                requests,
                name
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
                request,
                employee
            )

            save_approvals(
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

            print("1. Согласовать")
            print("2. Отклонить")

            decision_choice = input_int(
                "Выберите решение: "
            )

            if decision_choice == 1:
                if not approval.can_approve():
                    result = "Нет прав на согласование"

                elif approval.request.amount > budget:
                    result = "Недостаточно бюджета"

                else:
                    result = "Согласована"
                    budget -= approval.request.amount

            elif decision_choice == 2:
                result = "Отклонена"

            else:
                print("Такого решения нет")
                continue

            comment = input(
                "Комментарий: "
            )

            create_decision(
                decisions,
                approval,
                result,
                comment
            )

            save_requests(
                REQUESTS_FILE,
                requests
            )

            save_approvals(
                APPROVALS_FILE,
                approvals
            )

            save_decisions(
                DECISIONS_FILE,
                decisions
            )

            print("Результат:", result)
            print("Остаток бюджета:", budget)

        elif choice == 10:
            show_decisions(decisions)

        elif choice == 0:
            save_employees(
                EMPLOYEES_FILE,
                employees
            )

            save_requests(
                REQUESTS_FILE,
                requests
            )

            save_approvals(
                APPROVALS_FILE,
                approvals
            )

            save_decisions(
                DECISIONS_FILE,
                decisions
            )

            print("Программа завершена")
            break

        else:
            print("Такого пункта нет")


if __name__ == "__main__":
    main()
