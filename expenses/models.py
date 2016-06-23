from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _


class Income(models.Model):
    amount = models.IntegerField(_('amount'))
    date = models.DateField(_('income on'), default=timezone.now)

    class Meta:
        verbose_name = _('Income')
        verbose_name_plural = _('Incomes')

    def __str__(self):
        return "income ${self.amount} on {self.date}".format(self=self)


class Expense(models.Model):
    amount = models.IntegerField(_('amount'))
    date = models.DateField(_('expense on'),
                            default=timezone.now, db_index=True)
    purpose = models.CharField(_('purpose'), max_length=100)

    class Meta:
        verbose_name = _('Expense')
        verbose_name_plural = _('Expenses')

    def __str__(self):
        return "expended ${self.amount} on {self.date}".format(self=self)
