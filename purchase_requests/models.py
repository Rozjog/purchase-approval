from uuid import uuid4
from django.db import models, transaction
from django.db.models import Case, Value, When
from django.urls import reverse
from django.utils.text import slugify
from unidecode import unidecode


class RequestQuerySet(models.QuerySet):

    def created(self):
        return self.filter(status=self.model.Status.CREATED)

    def approved(self):
        return self.filter(status=self.model.Status.APPROVED)

    def rejected(self):
        return self.filter(status=self.model.Status.REJECTED)

    def cancelled(self):
        return self.filter(status=self.model.Status.CANCELLED)


RequestManager = models.Manager.from_queryset(RequestQuerySet)


class Request(models.Model):

    class Status(models.TextChoices):
        CREATED = "Создана", "Создана"
        APPROVED = "Одобрена", "Одобрена"
        REJECTED = "Отклонена", "Отклонена"
        CANCELLED = "Отменена", "Отменена"

    name = models.CharField(
        max_length=200,
        verbose_name="Название заявки",
    )

    amount = models.PositiveIntegerField(
        verbose_name="Сумма заявки",
        help_text=(
            "Укажите общую сумму закупки в рублях, "
            "без копеек."
        ),
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
        choices=Status.choices,
        default=Status.CREATED,
        verbose_name="Статус заявки",
    )

    requires_director = models.GeneratedField(
        expression=Case(
            When(amount__gt=250000, then=Value(True)),
            default=Value(False),
            output_field=models.BooleanField(),
        ),
        output_field=models.BooleanField(),
        db_persist=True,
        verbose_name="Требует согласования директора",
    )

    slug = models.SlugField(
        max_length=180,
        unique=True,
        editable=False,
        verbose_name="URL-идентификатор",
    )

    objects = RequestManager()

    def _build_slug(self):
        base_slug = slugify(unidecode(self.name)) or "request"
        suffix = f"-{self.pk}"

        base_slug = (
            base_slug[:180 - len(suffix)].rstrip("-")
            or "request"
        )

        return f"{base_slug}{suffix}"

    def save(self, *args, **kwargs):
        if self.slug:
            return super().save(*args, **kwargs)

        if self.pk is None:
            using = kwargs.get("using")

            with transaction.atomic(using=using):
                # Временный уникальный slug нужен
                # до получения ID новой заявки.
                self.slug = f"pending-{uuid4().hex}"

                super().save(*args, **kwargs)

                # После сохранения ID уже известен.
                self.slug = self._build_slug()

                return super().save(
                    update_fields=["slug"],
                    using=using,
                )

        self.slug = self._build_slug()

        if kwargs.get("update_fields") is not None:
            kwargs["update_fields"] = (
                set(kwargs["update_fields"]) | {"slug"}
            )

        return super().save(*args, **kwargs)

    def cancel(self):
        self.status = self.Status.CANCELLED
        self.save(update_fields=["status"])

    def get_absolute_url(self):
        return reverse(
            "purchase_requests:request_detail",
            kwargs={"slug": self.slug},
        )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["id"]
        verbose_name = "Заявка"
        verbose_name_plural = "Заявки"
