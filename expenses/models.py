from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _


class Balance(models.Model):
    INCOME = 0
    EXPENSE = 1
    BALANCE_KIND_CHOICES = (
        (INCOME, _('Income')),
        (EXPENSE, _('Expense')),
    )
    amount = models.IntegerField(_('amount'))
    kind = models.IntegerField(_('kind'),
                               choices=BALANCE_KIND_CHOICES,
                               default=INCOME)
    date = models.DateField(_('balance changed on'), default=timezone.now)
    notes = models.CharField(_('notes'), max_length=200)

    class Meta:
        verbose_name = _('Balance')
        verbose_name_plural = _('Balances')

    def __str__(self):
        return '+-'[self.kind] + str(self.amount)
