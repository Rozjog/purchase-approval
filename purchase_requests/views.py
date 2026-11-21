
from django.core.paginator import Paginator
from django.db.models import Count, Q, Sum
from django.shortcuts import (
    get_object_or_404,
    redirect,
    render,
)

from approvals.models import Approval
from employees.models import Employee

from .forms import RequestFilterForm, RequestForm
from .models import Request


def requests(request):
    form = RequestFilterForm(request.GET or None)
    form_valid = form.is_bound and form.is_valid()

    search = ""
    employee = ""
    min_amount = None
    status = ""
    sort = "id"
    error = ""

    if form_valid:
        search = form.cleaned_data.get("q") or ""
        employee = form.cleaned_data.get("employee") or ""
        min_amount = form.cleaned_data.get("min_amount")
        status = form.cleaned_data.get("status") or ""
        sort = form.cleaned_data.get("sort") or "id"

    elif form.is_bound:
        error = "Проверьте корректность параметров фильтрации."

    requests_list = Request.objects.select_related("employee")

    if search:
        requests_list = requests_list.filter(
            Q(name__icontains=search)
            | Q(contractor__icontains=search)
        )

    if employee:
        requests_list = requests_list.filter(
            employee__name__icontains=employee
        )

    if min_amount is not None:
        requests_list = requests_list.filter(
            amount__gte=min_amount
        )

    if status:
        requests_list = requests_list.filter(
            status=status
        )

    sort_fields = {
        "id": "id",
        "name": "name",
        "amount_asc": "amount",
        "amount_desc": "-amount",
        "employee": "employee__name",
    }

    requests_list = requests_list.order_by(
        sort_fields.get(sort, "id"),
        "id",
    )

    paginator = Paginator(requests_list, 5)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "requests": page_obj,
        "page_obj": page_obj,
        "form": form,
        "error": error,
    }

    return render(
        request,
        "purchase_requests/request_list.html",
        context,
    )


def request_create(request):
    if request.method == "POST":
        form = RequestForm(request.POST)

        if form.is_valid():
            form.save()

            return redirect("purchase_requests:requests")

    else:
        form = RequestForm()

    return render(
        request,
        "purchase_requests/request_form.html",
        {"form": form},
    )


def request_detail(request, slug):
    purchase_request = get_object_or_404(
        Request.objects.select_related("employee"),
        slug=slug,
    )

    return render(
        request,
        "purchase_requests/request_detail.html",
        {"purchase_request": purchase_request},
    )


def request_detail_by_id(request, request_id):
    purchase_request = get_object_or_404(
        Request,
        pk=request_id,
    )

    return redirect(
        purchase_request.get_absolute_url()
    )


def statistics(request):
    total_requests = Request.objects.count()

    total_amount = Request.objects.aggregate(
        total=Sum("amount")
    )["total"] or 0

    request_statuses = (
        Request.objects
        .values("status")
        .annotate(requests_count=Count("id"))
        .order_by("-requests_count", "status")
    )

    approval_statuses = (
        Approval.objects
        .values("status")
        .annotate(approvals_count=Count("id"))
        .order_by("-approvals_count", "status")
    )

    top_requests = (
        Request.objects
        .exclude(status=Request.Status.CANCELLED)
        .order_by("-amount", "id")[:5]
    )

    approved_total = (
        Request.objects
        .approved()
        .aggregate(total=Sum("amount"))
    )["total"] or 0

    employee_counts = (
        Employee.objects
        .annotate(requests_count=Count("requests"))
        .order_by("-requests_count", "name")
    )

    context = {
        "total_requests": total_requests,
        "total_amount": total_amount,
        "request_statuses": request_statuses,
        "approval_statuses": approval_statuses,
        "top_requests": top_requests,
        "approved_total": approved_total,
        "employee_counts": employee_counts,
    }

    return render(
        request,
        "purchase_requests/statistics.html",
        context,
    )
