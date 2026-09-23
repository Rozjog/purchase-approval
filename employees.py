def create_employee(employees: list, name: str, role: str):
    employee = {
        "id": len(employees) + 1,
        "name": name,
        "role": role
    }

    employees.append(employee)
    return employee


def find_employee_by_id(employees: list, employee_id: int):
    for employee in employees:
        if employee["id"] == employee_id:
            return employee

    return None


def show_employees(employees: list):
    if not employees:
        print("Сотрудников нет")
        return

    for employee in employees:
        print(
            "ID:", employee["id"],
            "Имя:", employee["name"],
            "Роль:", employee["role"]
        )
        