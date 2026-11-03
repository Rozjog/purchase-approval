
from django.db import models, transaction


class Decision(models.Model):
    approval = models.ForeignKey(
        "approvals.Approval",
        on_delete=models.PROTECT,
        related_name="decisions",
        verbose_name="Согласование",
    )

    result = models.CharField(
        max_length=50,
        verbose_name="Результат решения",
    )

    comment = models.TextField(
        verbose_name="Комментарий",
    )

    def apply(self):
        with transaction.atomic():
            self.approval.status = self.result
            self.approval.save(update_fields=["status"])

            purchase_request = self.approval.request
            purchase_request.status = self.result
            purchase_request.save(update_fields=["status"])

    def __str__(self):
        return f"Решение №{self.pk}"

    class Meta:
        ordering = ["id"]
        verbose_name = "Решение"
        verbose_name_plural = "Решения"
