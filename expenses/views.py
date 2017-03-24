from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

from .models import Balance


class BalanceView(LoginRequiredMixin, ListView):
    model = Balance

    def get_context_data(self):
        context = super().get_context_data()
        context.update({'current_balance': Balance.current()})
        return context
