from django.db import models


class Employee(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name="Имя сотрудника",
    )

    role = models.CharField(
        max_length=100,
        verbose_name="Должность",
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]
        verbose_name = "Сотрудник"
        verbose_name_plural = "Сотрудники"
