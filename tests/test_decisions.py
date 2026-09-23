from decisions import create_decision, find_decision_by_id


def test_create_decision() -> None:
    decisions: list[dict] = []

    create_decision(
        decisions,
        1,
        "Одобрено",
        "Закупка согласована"
    )

    assert len(decisions) == 1
    assert decisions[0]["approval_id"] == 1
    assert decisions[0]["result"] == "Одобрено"


def test_find_decision_by_id() -> None:
    decisions: list[dict] = []

    create_decision(
        decisions,
        1,
        "Одобрено",
        "Закупка согласована"
    )

    decision = find_decision_by_id(decisions, 1)

    assert decision is not None
    assert decision["id"] == 1


def test_decision_not_found() -> None:
    decisions: list[dict] = []

    decision = find_decision_by_id(decisions, 10)

    assert decision is None