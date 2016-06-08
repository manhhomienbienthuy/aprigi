from django.db.models import Sum
from django.utils import timezone

from .models import Objective, Passbook, Withdraw


def savings(request):
    withdrawn = Withdraw.objects.filter(is_open=True).aggregate(
        Sum('amount')).get('amount__sum') or 0
    current = Passbook.objects.filter(is_open=True).aggregate(
        Sum('amount')).get('amount__sum') or 0
    try:
        objective = Objective.objects.get(year=timezone.now().year).amount
    except Objective.DoesNotExist:
        objective = 0
    try:
        percentage = current / objective * 100
    except ZeroDivisionError:
        percentage = 0

    return {
        'withdrawn': withdrawn,
        'objective': objective,
        'current': current,
        'percentage': "%.2f%%" % percentage,
    }
