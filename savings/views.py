from django.views.generic.list import ListView

from .models import Passbook


class PassbookView(ListView):
    model = Passbook
