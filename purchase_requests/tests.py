
from django.test import TestCase
from django.urls import reverse

from employees.models import Employee
from .models import Request


class RequestTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.employee = Employee.objects.create(
            name="Иван Иванов",
            role="Руководитель отдела",
        )

        cls.request1 = Request.objects.create(
            name="Покупка канцтоваров",
            amount=20000,
            contractor="Комус",
            employee=cls.employee,
        )

        cls.request2 = Request.objects.create(
            name="Закупка ноутбуков",
            amount=300000,
            contractor="DNS",
            employee=cls.employee,
            status=Request.Status.APPROVED,
        )

        cls.request3 = Request.objects.create(
            name="Покупка принтера",
            amount=45000,
            contractor="Ситилинк",
            employee=cls.employee,
            status=Request.Status.CANCELLED,
        )

    def test_custom_queryset(self):
        """Проверка пользовательского менеджера."""
        self.assertEqual(Request.objects.created().count(), 1)
        self.assertEqual(Request.objects.approved().count(), 1)
        self.assertEqual(Request.objects.cancelled().count(), 1)

    def test_amount_filter(self):
        """Проверка фильтрации по минимальной сумме."""
        response = self.client.get(
            reverse("purchase_requests:requests"),
            {"min_amount": "100000"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Закупка ноутбуков")
        self.assertNotContains(response, "Покупка канцтоваров")

    def test_search(self):
        """Проверка поиска по названию заявки."""
        response = self.client.get(
            reverse("purchase_requests:requests"),
            {"q": "ноут"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Закупка ноутбуков")
        self.assertNotContains(response, "Покупка принтера")

    def test_generated_field(self):
        """Проверка вычисляемого поля базы данных."""
        self.request1.refresh_from_db()
        self.request2.refresh_from_db()

        self.assertFalse(self.request1.requires_director)
        self.assertTrue(self.request2.requires_director)

    def test_slug_and_absolute_url(self):
        """Проверка slug и подробной страницы."""
        self.assertTrue(self.request1.slug)
        self.assertTrue(
            self.request1.slug.endswith(
                f"-{self.request1.pk}"
            )
        )

        url = self.request1.get_absolute_url()

        self.assertIn(self.request1.slug, url)

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Покупка канцтоваров")

    def test_missing_request(self):
        """Несуществующий slug должен возвращать HTTP 404."""
        url = reverse(
            "purchase_requests:request_detail",
            kwargs={"slug": "not-existing-request-99999"},
        )

        response = self.client.get(url)

        self.assertEqual(response.status_code, 404)

    def test_pagination(self):
        """На странице отображается не более пяти заявок."""
        for number in range(4):
            Request.objects.create(
                name=f"Тестовая закупка {number}",
                amount=1000,
                contractor="Тестовый контрагент",
                employee=self.employee,
            )

        url = reverse("purchase_requests:requests")

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            len(response.context["page_obj"].object_list),
            5,
        )

        response_page2 = self.client.get(
            url,
            {"page": "2"},
        )

        self.assertEqual(response_page2.status_code, 200)
        self.assertEqual(
            len(response_page2.context["page_obj"].object_list),
            2,
        )
