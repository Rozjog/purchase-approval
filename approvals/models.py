
from django.db import models


class Approval(models.Model):
    request = models.ForeignKey(
        "purchase_requests.Request",
        on_delete=models.PROTECT,
        related_name="approvals",
        verbose_name="Заявка",
    )

    employee = models.ForeignKey(
        "employees.Employee",
        on_delete=models.PROTECT,
        related_name="assigned_approvals",
        verbose_name="Ответственный сотрудник",
    )

    status = models.CharField(
        max_length=50,
        default="Ожидает решения",
        verbose_name="Статус согласования",
    )

    def can_approve(self):
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

    def __str__(self):
        return f"Согласование №{self.pk}"

    class Meta:
        ordering = ["id"]
        verbose_name = "Согласование"
        verbose_name_plural = "Согласования"
