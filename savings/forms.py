from django.forms import ModelForm

from .models import Passbook


class PassbookForm(ModelForm):

    class Meta:
        model = Passbook
        fields = '__all__'
