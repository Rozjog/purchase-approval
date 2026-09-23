def create_decision(decisions: list, approval_id: int, result: str, comment: str):
    decision = {
        "id": len(decisions) + 1,
        "approval_id": approval_id,
        "result": result,
        "comment": comment
    }

    decisions.append(decision)
    return decision


def find_decision_by_id(decisions: list, decision_id: int):
    for decision in decisions:
        if decision["id"] == decision_id:
            return decision

    return None


def show_decisions(decisions: list) -> None:
    if not decisions:
        print("Решений нет")
        return

    for decision in decisions:
        print(
            "ID:", decision["id"],
            "Согласование:", decision["approval_id"],
            "Результат:", decision["result"],
            "Комментарий:", decision["comment"]
        )