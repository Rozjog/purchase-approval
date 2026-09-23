from .employees import Employee
from .requests import Request


class Approval:
    def __init__(
        self,
        approval_id: int,
        request: Request,
        employee: Employee
    ) -> None:
        self.id = approval_id
        self.request = request
        self.employee = employee
        self.status = "Ожидает решения"

    def can_approve(self) -> bool:
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

    def __str__(self) -> str:
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
) -> Approval:
    approval = Approval(
        len(approvals) + 1,
        request,
        employee
    )

    approvals.append(approval)
    return approval


def find_approval_by_id(
    approvals: list[Approval],
    approval_id: int
) -> Approval | None:
    for approval in approvals:
        if approval.id == approval_id:
            return approval

    return None


def show_approvals(approvals: list[Approval]) -> None:
    if not approvals:
        print("Согласований нет")
        return

    for approval in approvals:
        print(approval)
