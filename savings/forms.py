from django import forms
from django.core.exceptions import SuspiciousOperation
from django.utils import timezone

from .models import Passbook, Withdraw


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

    def do_withdraw(self):
        object_list = self.get_passbook_list()
        total = sum(passbook.amount + passbook.interest_on_withdraw(
            self.cleaned_data['date']) for passbook in object_list)
        object_list.update(is_open=False)
        return Withdraw.objects.create(
            amount=total,
            date=self.cleaned_data['date'],
            is_open=True,
        )
