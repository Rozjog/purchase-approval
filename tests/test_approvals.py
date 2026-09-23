from approvals import create_approval, find_approval_by_id


def test_create_approval() -> None:
    approvals: list[dict] = []

    create_approval(
        approvals,
        1,
        2
    )

    assert len(approvals) == 1
    assert approvals[0]["request_id"] == 1
    assert approvals[0]["employee_id"] == 2
    assert approvals[0]["status"] == "Ожидает решения"


def test_find_approval_by_id() -> None:
    approvals: list[dict] = []

    create_approval(
        approvals,
        1,
        2
    )

    approval = find_approval_by_id(approvals, 1)

    assert approval is not None
    assert approval["id"] == 1


def test_approval_not_found() -> None:
    approvals: list[dict] = []

    approval = find_approval_by_id(approvals, 10)

    assert approval is None