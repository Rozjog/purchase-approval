
from django.db import migrations, models
from django.db.models import Case, Value, When
from django.utils.text import slugify

from unidecode import unidecode


def populate_slugs(apps, schema_editor):
    Request = apps.get_model(
        "purchase_requests",
        "Request",
    )

    database = schema_editor.connection.alias

    for obj in Request.objects.using(database).order_by("pk"):
        suffix = f"-{obj.pk}"
        base = slugify(unidecode(obj.name)) or "request"
        base = base[:180 - len(suffix)].rstrip("-") or "request"

        Request.objects.using(database).filter(
            pk=obj.pk,
        ).update(
            slug=f"{base}{suffix}",
        )


class Migration(migrations.Migration):

    dependencies = [
        ("purchase_requests", "0003_request_enhancements"),
    ]

    operations = [
        migrations.AddField(
            model_name="request",
            name="slug",
            field=models.SlugField(
                max_length=180,
                blank=True,
                null=True,
                editable=False,
                verbose_name="URL-идентификатор",
            ),
        ),

        migrations.RunPython(
            populate_slugs,
            migrations.RunPython.noop,
        ),

        migrations.AlterField(
            model_name="request",
            name="slug",
            field=models.SlugField(
                max_length=180,
                unique=True,
                editable=False,
                verbose_name="URL-идентификатор",
            ),
        ),

        migrations.AddField(
            model_name="request",
            name="requires_director",
            field=models.GeneratedField(
                expression=Case(
                    When(
                        amount__gt=250000,
                        then=Value(True),
                    ),
                    default=Value(False),
                    output_field=models.BooleanField(),
                ),
                output_field=models.BooleanField(),
                db_persist=True,
                verbose_name="Требует согласования директора",
            ),
        ),

        migrations.AlterField(
            model_name="request",
            name="status",
            field=models.CharField(
                max_length=50,
                choices=[
                    ("Создана", "Создана"),
                    ("Одобрена", "Одобрена"),
                    ("Отклонена", "Отклонена"),
                    ("Отменена", "Отменена"),
                ],
                default="Создана",
                verbose_name="Статус заявки",
            ),
        ),
    ]
