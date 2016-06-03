from django import forms

from .models import Passbook


class PassbookForm(forms.ModelForm):

    class Meta:
        model = Passbook
        fields = '__all__'


class PassbookSearchForm(forms.Form):
    is_open = forms.NullBooleanField()
    upcoming = forms.DateField(required=False)


class PassbookWithdrawForm(forms.Form):
    date = forms.DateField(required=True)
