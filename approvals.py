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