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
                               default=INCOME,
                               db_index=True)
    date = models.DateField(_('balance changed on'), default=timezone.now,
                            db_index=True)
    notes = models.CharField(_('notes'), max_length=200)

    class Meta:
        verbose_name = _('Balance')
        verbose_name_plural = _('Balances')

    def __str__(self):
        return '+-'[self.kind] + str(self.amount)

    @classmethod
    def current(cls):
        return cls.total_income() - cls.total_expense()

    @classmethod
    def total_income(cls):
        return cls.objects.filter(kind=cls.INCOME).aggregate(
            models.Sum('amount')).get('amount__sum') or 0

    @classmethod
    def total_expense(cls):
        return cls.objects.filter(kind=cls.EXPENSE).aggregate(
            models.Sum('amount')).get('amount__sum') or 0
