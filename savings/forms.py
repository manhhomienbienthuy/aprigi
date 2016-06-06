from django import forms
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
