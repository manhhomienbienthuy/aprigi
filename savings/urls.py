from django.conf.urls import url

from .views import PassbookView

app_name = 'savings'
urlpatterns = [
    url(r'^$', PassbookView.as_view(), name='index'),
]
