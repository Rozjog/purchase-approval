
from django.db import models


class Request(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name="Название заявки",
    )

    amount = models.PositiveIntegerField(
        verbose_name="Сумма заявки",
    )

    contractor = models.CharField(
        max_length=200,
        verbose_name="Контрагент",
    )

    employee = models.ForeignKey(
        "employees.Employee",
        on_delete=models.PROTECT,
        related_name="requests",
        verbose_name="Автор заявки",
    )

    status = models.CharField(
        max_length=50,
        default="Создана",
        verbose_name="Статус заявки",
    )

    def cancel(self):
        self.status = "Отменена"
        self.save(update_fields=["status"])

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["id"]
        verbose_name = "Заявка"
        verbose_name_plural = "Заявки"
