from models.employees import (
    create_employee,
    find_employee_by_id
)


def test_create_employee() -> None:
    employees: list = []

    employee = create_employee(
        employees,
        "Иван Иванов",
        "Директор"
    )

    assert len(employees) == 1
    assert employee.id == 1
    assert employee.name == "Иван Иванов"
    assert employee.role == "Директор"


def test_find_employee_by_id() -> None:
    employees: list = []

    create_employee(
        employees,
        "Иван Иванов",
        "Директор"
    )

    employee = find_employee_by_id(
        employees,
        1
    )

    assert employee is not None
    assert employee.name == "Иван Иванов"


def test_employee_not_found() -> None:
    employees: list = []

    employee = find_employee_by_id(
        employees,
        10
    )

    assert employee is None
