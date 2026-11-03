
from django.shortcuts import get_object_or_404, render

from employees.models import Employee


def employees(request):
    employees_list = Employee.objects.order_by("name")

    context = {
        "employees": employees_list,
    }

    return render(
        request,
        "employees/employee_list.html",
        context,
    )


def employee_detail(request, employee_id):
    employee = get_object_or_404(
        Employee,
        pk=employee_id,
    )

    context = {
        "employee": employee,
    }

    return render(
        request,
        "employees/employee_detail.html",
        context,
    )
