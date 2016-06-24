from django.conf.urls import url
from django.core.urlresolvers import reverse_lazy
from django.views.generic import RedirectView

from .views import BalanceView

app_name = 'expenses'

urlpatterns = [
    url(r'^$', RedirectView.as_view(url=reverse_lazy('expenses:balance_list')),
        name='index'),
    url(r'^balance/$', BalanceView.as_view(), name='balance_list'),
]
