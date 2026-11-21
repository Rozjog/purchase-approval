from django.test import TestCase
from django.urls import reverse
from employees.models import Employee
from .models import Request
from io import BytesIO
from tempfile import TemporaryDirectory
from PIL import Image
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import override_settings
from approvals.models import Approval


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


class RequestFormScenarioTests(TestCase):

    def setUp(self):
        self.employee = Employee.objects.create(
            name="Тестовый сотрудник",
            role="Руководитель отдела",
        )

        self.purchase_request = Request.objects.create(
            name="Тестовая заявка",
            amount=20000,
            contractor="Тестовый поставщик",
            employee=self.employee,
        )

        self.valid_data = {
            "name": "Закупка оборудования",
            "amount": "300000",
            "contractor": "Новый поставщик",
            "employee": str(self.employee.pk),
        }

    def test_create_request(self):

        url = reverse("purchase_requests:request_create")
        old_count = Request.objects.count()

        response = self.client.post(url, self.valid_data)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            Request.objects.count(),
            old_count + 1,
        )

        created = Request.objects.latest("id")

        self.assertEqual(created.status, Request.Status.CREATED)
        self.assertEqual(created.amount, 300000)
        self.assertTrue(created.slug)

        created.refresh_from_db()
        self.assertTrue(created.requires_director)

    def test_invalid_amount(self):

        url = reverse("purchase_requests:request_create")

        data = {
            **self.valid_data,
            "amount": "0",
        }

        old_count = Request.objects.count()
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            Request.objects.count(),
            old_count,
        )

        self.assertIn(
            "amount",
            response.context["form"].errors,
        )

    def test_update_request(self):

        url = reverse(
            "purchase_requests:request_update",
            args=[self.purchase_request.pk],
        )

        old_slug = self.purchase_request.slug
        old_count = Request.objects.count()

        response = self.client.post(url, self.valid_data)

        self.assertEqual(response.status_code, 302)

        self.purchase_request.refresh_from_db()

        self.assertEqual(
            self.purchase_request.name,
            "Закупка оборудования",
        )
        self.assertEqual(self.purchase_request.amount, 300000)
        self.assertEqual(self.purchase_request.slug, old_slug)
        self.assertEqual(Request.objects.count(), old_count)

    def test_update_missing_request(self):

        url = reverse(
            "purchase_requests:request_update",
            args=[999999],
        )

        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_update_with_approval_forbidden(self):

        Approval.objects.create(
            request=self.purchase_request,
            employee=self.employee,
        )

        url = reverse(
            "purchase_requests:request_update",
            args=[self.purchase_request.pk],
        )

        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_cancel_request(self):

        url = reverse(
            "purchase_requests:request_cancel",
            args=[self.purchase_request.pk],
        )

        old_count = Request.objects.count()

        response = self.client.post(url)

        self.assertEqual(response.status_code, 302)

        self.purchase_request.refresh_from_db()

        self.assertEqual(
            self.purchase_request.status,
            Request.Status.CANCELLED,
        )
        self.assertEqual(Request.objects.count(), old_count)

        # Повторная отмена недоступна.
        response = self.client.post(url)
        self.assertEqual(response.status_code, 404)

    def test_cancel_get_not_allowed(self):

        url = reverse(
            "purchase_requests:request_cancel",
            args=[self.purchase_request.pk],
        )

        response = self.client.get(url)

        self.assertEqual(response.status_code, 405)

        self.purchase_request.refresh_from_db()

        self.assertEqual(
            self.purchase_request.status,
            Request.Status.CREATED,
        )

    def test_invalid_filter(self):

        url = reverse("purchase_requests:requests")

        response = self.client.get(
            url,
            {"min_amount": "abc"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn(
            "min_amount",
            response.context["form"].errors,
        )

    def test_image_upload(self):

        with TemporaryDirectory() as media_dir:
            with override_settings(MEDIA_ROOT=media_dir):
                buffer = BytesIO()
                image = Image.new("RGB", (10, 10), "white")
                image.save(buffer, format="PNG")

                uploaded_image = SimpleUploadedFile(
                    "test.png",
                    buffer.getvalue(),
                    content_type="image/png",
                )

                data = {
                    **self.valid_data,
                    "image": uploaded_image,
                }

                url = reverse(
                    "purchase_requests:request_create"
                )

                response = self.client.post(url, data)

                self.assertEqual(response.status_code, 302)

                created = Request.objects.latest("id")

                self.assertTrue(created.image)
                self.assertTrue(
                    created.image.storage.exists(
                        created.image.name
                    )
                )

                detail = self.client.get(
                    created.get_absolute_url()
                )

                self.assertEqual(detail.status_code, 200)
                self.assertContains(
                    detail,
                    created.image.url,
                )
