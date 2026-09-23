from .employees import Employee


class Request:
    def __init__(
        self,
        request_id: int,
        name: str,
        amount: int,
        contractor: str,
        employee: Employee
    ) -> None:
        self.id = request_id
        self.name = name
        self.amount = amount
        self.contractor = contractor
        self.employee = employee
        self.status = "Создана"

    def cancel(self) -> None:
        self.status = "Отменена"

    def __str__(self) -> str:
        return (
            f"ID: {self.id}, "
            f"Название: {self.name}, "
            f"Сумма: {self.amount}, "
            f"Контрагент: {self.contractor}, "
            f"Сотрудник: {self.employee.name}, "
            f"Статус: {self.status}"
        )


def create_request(
    requests: list[Request],
    name: str,
    amount: int,
    contractor: str,
    employee: Employee
) -> Request:

    request = Request(
        len(requests) + 1,
        name,
        amount,
        contractor,
        employee
    )

    requests.append(request)
    return request


def find_by_name(
    requests: list[Request],
    name: str
) -> Request | None:
    for request in requests:
        if name.lower() in request.name.lower():
            return request

    return None


def cancel_request(
    requests: list[Request],
    name: str
) -> bool:
    request = find_by_name(
        requests,
        name
    )

    if request is None:
        return False

    request.cancel()
    return True


def show_requests(
    requests: list[Request]
) -> None:
    if not requests:
        print("Заявок нет")
        return

    for request in requests:
        print(request)
