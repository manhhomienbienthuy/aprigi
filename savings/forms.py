from django import forms
from django.core.exceptions import SuspiciousOperation
from django.utils import timezone

from .models import Passbook


class PassbookForm(forms.ModelForm):

    class Meta:
        model = Passbook
        fields = '__all__'


class PassbookSearchForm(forms.Form):
    is_open = forms.NullBooleanField()
    upcoming = forms.DateField(
        required=False, initial=timezone.now().strftime('%Y-%m-%d'))


class PassbookWithdrawForm(forms.Form):
    date = forms.DateField(
        required=True, initial=timezone.now().strftime('%Y-%m-%d'))

    def get_passbook_list(self):
        object_list = Passbook.objects.all().filter(is_open=True)
        if not self.is_valid():
            raise SuspiciousOperation("Invalid date input")
        target_date = self.cleaned_data.get('date')
        return object_list.filter(stop_date__lte=target_date)
