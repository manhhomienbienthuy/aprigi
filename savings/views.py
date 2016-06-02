from calendar import monthrange
from datetime import timedelta

from django.core.urlresolvers import reverse
from django.utils import dateparse, timezone
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from .forms import PassbookForm
from .models import Passbook


class PassbookView(ListView):
    model = Passbook

    def get_queryset(self):
        object_list = self.model.objects.all().order_by('start_date')
        is_open = self.request.GET.get('is_open')
        if is_open is not None:
            object_list = object_list.filter(is_open__exact=is_open)
        target_date = self._upcoming_date(self.request.GET.get('upcoming'))
        if target_date:
            object_list = object_list.filter(is_open=True,
                                             stop_date__lte=target_date)
        return object_list

    def _upcoming_date(self, upcoming):
        if not upcoming:
            return None
        if upcoming not in ('thisweek', 'thismonth'):
            try:
                return dateparse.parse_date(upcoming)
            except ValueError:
                return None
        today = timezone.now()
        if upcoming == 'thismonth':
            end_date = monthrange(today.year, today.month)[1]
            return "{year}-{month}-{day}".format(
                year=today.year,
                month=today.month,
                day=end_date
            )
        return (today + timedelta(days=7)).date()


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
