from django import forms
from .models import Request
from django.core.files.uploadedfile import UploadedFile


class RequestFilterForm(forms.Form):
    q = forms.CharField(
        required=False,
        label="Название или контрагент",
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Введите текст для поиска",
            }
        ),
    )

    employee = forms.CharField(
        required=False,
        label="Имя сотрудника",
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Например, Иван",
            }
        ),
    )

    min_amount = forms.IntegerField(
        required=False,
        min_value=0,
        label="Минимальная сумма",
        error_messages={
            "invalid": "Введите целую сумму.",
            "min_value": "Сумма не может быть отрицательной.",
        },
        widget=forms.NumberInput(
            attrs={
                "class": "form-control",
                "placeholder": "Например, 10000",
                "min": 0,
            }
        ),
    )

    status = forms.ChoiceField(
        required=False,
        label="Статус заявки",
        choices=[
            ("", "Все статусы"),
            *Request.Status.choices,
        ],
        widget=forms.Select(
            attrs={"class": "form-select"}
        ),
    )

    sort = forms.ChoiceField(
        required=False,
        initial="id",
        label="Сортировать по",
        choices=[
            ("id", "Идентификатору"),
            ("name", "Названию"),
            ("amount_asc", "Сумме (по возрастанию)"),
            ("amount_desc", "Сумме (по убыванию)"),
            ("employee", "Имени сотрудника"),
        ],
        widget=forms.Select(
            attrs={"class": "form-select"}
        ),
    )


class RequestForm(forms.ModelForm):

    class Meta:
        model = Request

        fields = [
            "name",
            "amount",
            "contractor",
            "employee",
            "image",
        ]

        labels = {
            "name": "Название заявки",
            "amount": "Сумма закупки",
            "contractor": "Контрагент",
            "employee": "Сотрудник",
            "image": "Изображение заявки",
        }

        help_texts = {
            "name": "Укажите, что необходимо закупить.",
            "amount": (
                "Введите общую сумму закупки в рублях. "
                "Сумма должна быть больше нуля."
            ),
            "contractor": (
                "Укажите организацию или поставщика."
            ),
            "employee": (
                "Выберите сотрудника, создавшего заявку."
            ),
            "image": (
                "Необязательное изображение товара или оборудования. "
                "Допустимые форматы: JPG, PNG, WebP. До 5 МБ."
            ),
        }

        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Например, закупка ноутбуков",
                }
            ),
            "amount": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": 1,
                    "placeholder": "Введите сумму в рублях",
                }
            ),
            "contractor": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Название контрагента",
                }
            ),
            "employee": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),
            "image": forms.ClearableFileInput(
                attrs={
                    "class": "form-control",
                    "accept": "image/jpeg,image/png,image/webp",
                }
            ),
        }

    def clean_amount(self):
        amount = self.cleaned_data["amount"]

        if amount <= 0:
            raise forms.ValidationError(
                "Сумма закупки должна быть больше нуля."
            )

        return amount


    def clean_image(self):
        image = self.cleaned_data.get("image")

        if isinstance(image, UploadedFile):
            # Максимальный размер — 5 МБ.
            if image.size > 5 * 1024 * 1024:
                raise forms.ValidationError(
                    "Размер изображения не должен превышать 5 МБ."
                )

            # Проверяем формат изображения через Pillow.
            if image.image.format not in ("JPEG", "PNG", "WEBP"):
                raise forms.ValidationError(
                    "Разрешены только JPG, PNG и WebP."
                )

        return image
