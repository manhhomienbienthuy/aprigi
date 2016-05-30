from django.db import models
from django.utils.translation import ugettext_lazy as _


class Passbook(models.Model):
    WEEK = 1
    MONTH = 2
    PERIOD_TYPE_CHOICES = (
        (WEEK, 'Week'),
        (MONTH, 'Month'),
    )
    DEFAULT_PERIOD_TYPE = MONTH

    number = models.CharField(_('number'), max_length=30, unique=True,
                              db_index=True)
    account_number = models.CharField(_('account number'),
                                      max_length=30, unique=True,
                                      db_index=True)
    amount = models.IntegerField(_('amount'))
    period_type = models.IntegerField(_('period type'),
                                      choices=PERIOD_TYPE_CHOICES,
                                      default=DEFAULT_PERIOD_TYPE)
    period = models.IntegerField(_('period'))
    rate = models.FloatField(_('rate'))
    start_date = models.DateField(_('start date'))
    stop_date = models.DateField(_('stop date'))
    is_open = models.BooleanField(_('is open'), default=True,
                                  db_index=True)
    notes = models.CharField(_('notes'), max_length=200)

    class Meta:
        verbose_name = _('Passbook')
        verbose_name_plural = _('Passbooks')

    def __str__(self):
        return self.number
