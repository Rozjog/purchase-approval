
from purchase_requests.models import Request


def purchase_context(request):
    """Общие данные для шаблонов Purchase Approval."""
    return {
        "site_name": "Purchase Approval",
        "requests_count": Request.objects.count(),
    }
