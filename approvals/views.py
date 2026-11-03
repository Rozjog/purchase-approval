from django.shortcuts import get_object_or_404, render
from approvals.models import Approval


def approvals(request):
    approvals_list = Approval.objects.select_related(
        "request",
        "employee",
    ).order_by("id")

    context = {
        "approvals": approvals_list,
    }

    return render(
        request,
        "approvals/approval_list.html",
        context,
    )


def approval_detail(request, approval_id):
    approval = get_object_or_404(
        Approval.objects.select_related(
            "request",
            "employee",
        ),
        pk=approval_id,
    )

    context = {
        "approval": approval,
    }

    return render(
        request,
        "approvals/approval_detail.html",
        context,
    )
