from requests import create_request, find_by_name, cancel_request


def test_create_request() -> None:
    requests: list[dict] = []

    create_request(
        requests,
        "Покупка ноутбуков",
        180000,
        "ООО Техно"
    )

    assert len(requests) == 1
    assert requests[0]["name"] == "Покупка ноутбуков"


def test_find_by_name() -> None:
    requests: list[dict] = []

    create_request(
        requests,
        "Покупка ноутбуков",
        180000,
        "ООО Техно"
    )

    request = find_by_name(requests, "ноутбуков")

    assert request is not None
    assert request["name"] == "Покупка ноутбуков"


def test_cancel_request() -> None:
    requests: list[dict] = []

    create_request(
        requests,
        "Покупка ноутбуков",
        180000,
        "ООО Техно"
    )

    cancel_request(requests, "ноутбуков")

    assert requests[0]["status"] == "Отменена"
