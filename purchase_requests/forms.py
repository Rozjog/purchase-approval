from django import forms
from .models import Request


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
