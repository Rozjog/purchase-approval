class Employee:
    def __init__(
        self,
        employee_id: int,
        name: str,
        role: str
    ) -> None:
        self.id = employee_id
        self.name = name
        self.role = role

    def __str__(self) -> str:
        return (
            f"ID: {self.id}, "
            f"Имя: {self.name}, "
            f"Роль: {self.role}"
        )


def create_employee(
    employees: list[Employee],
    name: str,
    role: str
) -> Employee:
    employee = Employee(
        len(employees) + 1,
        name,
        role
    )

    employees.append(employee)
    return employee


def find_employee_by_id(
    employees: list[Employee],
    employee_id: int
) -> Employee | None:
    for employee in employees:
        if employee.id == employee_id:
            return employee

    return None


def show_employees(
    employees: list[Employee]
) -> None:
    if not employees:
        print("Сотрудников нет")
        return

    for employee in employees:
        print(employee)
