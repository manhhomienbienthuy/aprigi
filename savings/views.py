from calendar import monthrange
from datetime import timedelta

from django.utils import timezone
from django.views.generic.list import ListView

from .models import Passbook


class PassbookView(ListView):
    model = Passbook

    def get_queryset(self):
        objects_list = self.model.objects.all().order_by('start_date')
        is_open = self.request.GET.get('is_open')
        if is_open is not None:
            objects_list = objects_list.filter(is_open__exact=is_open)
        upcoming = self.request.GET.get('upcoming')
        if upcoming:
            if upcoming not in ('today', 'thisweek', 'thismonth'):
                target_date = upcoming
            else:
                today = timezone.now()
                if upcoming == 'today':
                    target_date = today.date()
                elif upcoming == 'thisweek':
                    target_date = (today + timedelta(days=7)).date()
                elif upcoming == 'thismonth':
                    end_date = monthrange(today.year, today.month)[1]
                    target_date = "{year}-{month}-{day}".format(
                        year=today.year,
                        month=today.month,
                        day=end_date
                    )
            objects_list = objects_list.filter(is_open=True,
                                               stop_date__lte=target_date)
        return objects_list
