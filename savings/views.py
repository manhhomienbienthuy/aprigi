from calendar import monthrange
from datetime import timedelta

from django.core.urlresolvers import reverse
from django.utils import timezone
from django.views.generic import (CreateView, DeleteView, FormView, ListView,
                                  UpdateView)

from .forms import PassbookForm, PassbookSearchForm, PassbookWithdrawForm
from .models import Passbook


class PassbookView(ListView):
    model = Passbook

    def get_queryset(self):
        object_list = self.model.objects.all().order_by('start_date')
        form = PassbookSearchForm(self.request.GET or None)
        if form.is_valid():
            is_open = form.cleaned_data.get('is_open')
            if is_open is not None:
                object_list = object_list.filter(is_open=is_open)
            target_date = form.cleaned_data.get('upcoming')
            if target_date:
                object_list = object_list.filter(is_open=True,
                                                 stop_date__lte=target_date)
        return object_list

    def get_context_data(self):
        context = super().get_context_data()
        context.update(self._upcoming_date())
        submitted_date = self.request.GET.get(
            'upcoming', timezone.now().strftime('%Y-%m-%d'))
        context.update({
            'form': PassbookSearchForm({'upcoming': submitted_date}),
        })
        return context

    def _upcoming_date(self):
        today = timezone.now()
        end_date_of_month = monthrange(today.year, today.month)[1]
        end_of_month = "{year:04d}-{month:02d}-{day:02d}".format(
            year=today.year,
            month=today.month,
            day=end_date_of_month,
        )
        return {
            'thisweek': (today + timedelta(days=7)).strftime('%Y-%m-%d'),
            'thismonth': end_of_month
        }


class PassbookCreateView(CreateView):
    model = Passbook
    form_class = PassbookForm

    def get_success_url(self):
        return reverse('savings:passbook_list')


class PassbookUpdateView(UpdateView):
    model = Passbook
    form_class = PassbookForm

    def get_success_url(self):
        return reverse('savings:passbook_list')


class PassbookDeleteView(DeleteView):
    model = Passbook

    def get_success_url(self):
        return reverse('savings:passbook_list')


class PassbookWithdrawView(FormView):
    form_class = PassbookWithdrawForm
    template_name = 'savings/passbook_withdraw.html'

    def get_context_data(self):
        context = super().get_context_data()
        form = self.form_class(self.request.GET or None)
        context.update({
            'object_list': form.get_passbook_list(),
            'form': form,
        })
        return context

    def form_valid(self, form):
        # Implement later
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('savings:passbook_list')
