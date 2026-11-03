
from django.shortcuts import get_object_or_404, render

from decisions.models import Decision


def decisions(request):
    decisions_list = Decision.objects.select_related(
        "approval__request"
    ).order_by("id")

    context = {
        "decisions": decisions_list,
    }

    return render(
        request,
        "decisions/decision_list.html",
        context,
    )


def decision_detail(request, decision_id):
    decision = get_object_or_404(
        Decision.objects.select_related(
            "approval__request"
        ),
        pk=decision_id,
    )

    context = {
        "decision": decision,
    }

    return render(
        request,
        "decisions/decision_detail.html",
        context,
    )
