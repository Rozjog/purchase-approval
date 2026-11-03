from django.shortcuts import get_object_or_404, render
from db.database import get_connection
from purchase_requests.models import Request
from django.db.models import Count, Q, Sum
from approvals.models import Approval
from django.core.paginator import Paginator



def requests(request):
    search = request.GET.get("q", "").strip()
    employee = request.GET.get("employee", "").strip()
    min_amount_text = request.GET.get("min_amount", "").strip()
    status = request.GET.get("status", "").strip()

    sort = request.GET.get("sort", "id")

    error = ""

    requests_list = Request.objects.select_related(
        "employee"
    )
    
    paginator = Paginator(requests_list, 2)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    if search:
        requests_list = requests_list.filter(
            Q(name__icontains=search)
            | Q(contractor__icontains=search)
        )

    if employee:
        requests_list = requests_list.filter(
            employee__name__icontains=employee
        )

    if min_amount_text:
        try:
            min_amount = int(min_amount_text)

            if min_amount < 0:
                raise ValueError

            requests_list = requests_list.filter(
                amount__gte=min_amount
            )

        except ValueError:
            error = "Введите неотрицательную целую сумму."

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

    if sort not in sort_fields:
        sort = "id"

    requests_list = requests_list.order_by(
        sort_fields[sort],
        "id",
    )

    context = {
        "requests": page_obj,
        "page_obj": page_obj,
        "search": search,
        "employee": employee,
        "min_amount": min_amount_text,
        "selected_status": status,
        "sort": sort,
        "error": error,
    }

    return render(
        request,
        "purchase_requests/request_list.html",
        context,
    )


def request_detail(request, request_id):
    purchase_request = get_object_or_404(
        Request.objects.select_related("employee"),
        pk=request_id,
    )

    context = {
        "purchase_request": purchase_request,
    }

    return render(
        request,
        "purchase_requests/request_detail.html",
        context,
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
        .exclude(status="Отменена")
        .order_by("-amount", "id")[:5]
    )

    context = {
        "total_requests": total_requests,
        "total_amount": total_amount,
        "request_statuses": request_statuses,
        "approval_statuses": approval_statuses,
        "top_requests": top_requests,
    }

    return render(
        request,
        "purchase_requests/statistics.html",
        context,
    )

