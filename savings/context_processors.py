from .models import Withdraw


def savings(request):
    open_withdraws = Withdraw.objects.filter(is_open=True)
    withdrawn = sum(withdraw.amount for withdraw in open_withdraws)
    return {
        'withdrawn': withdrawn,
        'goal': 100,
        'current': 75,
        'goal_percentage': '75%'
    }
