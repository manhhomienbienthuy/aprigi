from django.conf.urls import url
from django.core.urlresolvers import reverse_lazy
from django.views.generic import RedirectView

from .views import PassbookCreateView, PassbookUpdateView, PassbookView

app_name = 'savings'

urlpatterns = [
    url(r'^$', RedirectView.as_view(url=reverse_lazy('savings:passbook_list')),
        name='index'),
    url(r'^passbook/$', PassbookView.as_view(), name='passbook_list'),
    url(r'^passbook/create$', PassbookCreateView.as_view(),
        name='passbook_create'),
    url(r'^passbook/(?P<pk>\d+)/update$', PassbookUpdateView.as_view(),
        name='passbook_update')
]
