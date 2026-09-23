from .approvals import Approval


class Decision:
    def __init__(
        self,
        decision_id: int,
        approval: Approval,
        result: str,
        comment: str
    ):
        
        self.id = decision_id
        self.approval = approval
        self.result = result
        self.comment = comment

    def apply(self):
        self.approval.status = self.result
        self.approval.request.status = self.result

    def __str__(self):
        return (
            f"ID: {self.id}, "
            f"Согласование: {self.approval.id}, "
            f"Результат: {self.result}, "
            f"Комментарий: {self.comment}"
        )


def create_decision(
    decisions: list[Decision],
    approval: Approval,
    result: str,
    comment: str
):
    
    decision = Decision(
        len(decisions) + 1,
        approval,
        result,
        comment
    )

    decision.apply()

    decisions.append(decision)
    return decision


def find_decision_by_id(decisions: list[Decision], decision_id: int):
    for decision in decisions:
        if decision.id == decision_id:
            return decision

    return None


def show_decisions(decisions: list[Decision]):
    
    if not decisions:
        print("Решений нет")
        return

    for decision in decisions:
        print(decision)