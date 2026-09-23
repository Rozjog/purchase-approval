def create_approval(approvals: list, request_id: int, employee_id: int):
    approval = {
        "id": len(approvals) + 1,
        "request_id": request_id,
        "employee_id": employee_id,
        "status": "Ожидает решения"
    }

    approvals.append(approval)
    return approval


def find_approval_by_id(approvals: list, approval_id: int):
    for approval in approvals:
        if approval["id"] == approval_id:
            return approval

    return None


def can_approve(request: dict, role: str):

    if request["amount"] <= 250000 and role == "Руководитель отдела":
        return True

    if request["amount"] > 250000 and role == "Директор":
        return True

    return False


def approve_request(request: dict, budget: int, role: str):

    if not can_approve(request, role):
        request["status"] = "Нет прав на согласование"
        return budget

    if check_budget(request["amount"], budget):
        request["status"] = "Согласована"
        budget -= request["amount"]
    else:
        request["status"] = "Недостаточно бюджета"

    return budget


def check_budget(amount: int, budget: int):

    if amount <= budget:
        return True

    return False


def show_approvals(approvals: list):
    if not approvals:
        print("Согласований нет")
        return

    for approval in approvals:
        print(
            "ID:", approval["id"],
            "Заявка:", approval["request_id"],
            "Сотрудник:", approval["employee_id"],
            "Статус:", approval["status"]
        )