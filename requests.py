def create_request(requests: list, name: str, amount: int, contractor: str):

    request = {
        "id": len(requests) + 1,
        "name": name,
        "amount": amount,
        "contractor": contractor,
        "status": "Создана"
    }

    requests.append(request)

    return request


def find_request(requests: list, request_id: int):

    for request in requests:
        if request[id] == request_id:
            return request
    return None


def find_by_name(requests: list, name: str):

    for request in requests:
        if name.lower() in request[name]:
            return request
    return None


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


def can_approve(request: dict, role: str):

    if request["amount"] <= 250000 and role == "Руководитель отдела":
        return True

    if request["amount"] > 250000 and role == "Директор":
        return True

    return False

def cancel_request(requests: list, name: str):

    request = find_by_name(requests, name)

    if request is None:
        return False

    request["status"] = "Отменена"
    return True

def show_requests(requests: list) -> None:
    if not requests:
        print("Заявок нет")
        return

    for request in requests:
        print(
            "ID:", request["id"],
            "Название:", request["name"],
            "Сумма:", request["amount"],
            "Контрагент:", request["contractor"],
            "Статус:", request["status"]
        )