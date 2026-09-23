from .employees import Employee
from .requests import Request


class Approval:
    def __init__(
        self,
        approval_id: int,
        request: Request,
        employee: Employee
    ):
        self.id = approval_id
        self.request = request
        self.employee = employee
        self.status = "Ожидает решения"

    def can_approve(self):
        if (
            self.request.amount <= 250000
            and self.employee.role == "Руководитель отдела"
        ):
            return True

        if (
            self.request.amount > 250000
            and self.employee.role == "Директор"
        ):
            return True

        return False

    def __str__(self):
        return (
            f"ID: {self.id}, "
            f"Заявка: {self.request.name}, "
            f"Сотрудник: {self.employee.name}, "
            f"Статус: {self.status}"
        )


def create_approval(
    approvals: list[Approval],
    request: Request,
    employee: Employee
):
    approval = Approval(
        len(approvals) + 1,
        request,
        employee
    )

    approvals.append(approval)
    return approval


def find_approval_by_id(approvals: list[Approval], approval_id: int):
    for approval in approvals:
        if approval.id == approval_id:
            return approval

    return None


def show_approvals(approvals: list[Approval]):
    if not approvals:
        print("Согласований нет")
        return

    for approval in approvals:
        print(approval)
