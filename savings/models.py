from calendar import monthrange
from datetime import datetime

from django.db import models
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _

DAYS_PER_YEAR = 365
DAYS_PER_WEEK = 7
MONTHS_PER_YEAR = 12


class Passbook(models.Model):
    WEEK = 1
    MONTH = 2
    PERIOD_TYPE_CHOICES = (
        (WEEK, _('Week')),
        (MONTH, _('Month')),
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

    def interest(self):
        if not self.is_open or self.period_type not in (self.WEEK, self.MONTH):
            return None
        if self.period_type == self.WEEK:
            return round(self.amount * self.rate / 100 / DAYS_PER_YEAR *
                         self.period * 7)
        return round(self.amount * self.rate / 100 / MONTHS_PER_YEAR *
                     self.period)
    interest.short_description = _('interest (expected)')

    def interest_on_withdraw(self, date):
        if not self.is_open or self.period_type not in (self.WEEK, self.MONTH):
            return None

        RATE_OUT_PERIOD = 0.6
        base, interval_in_period, interval_out_period = self._get_info(date)
        total_after_period = self.amount * \
            (1 + self.rate / 100 / base * self.period) ** interval_in_period
        total = total_after_period * \
            (1 + RATE_OUT_PERIOD / 100 / DAYS_PER_YEAR) ** interval_out_period
        return round(total - self.amount)

    def _get_info(self, date):
        if self.period_type == self.WEEK:
            return self._get_info_week(date)
        else:
            return self._get_info_month(date)

    def _get_info_week(self, date):
        base = DAYS_PER_YEAR / DAYS_PER_WEEK
        interval = (date - self.start_date).days
        interval_in_period = interval // (DAYS_PER_WEEK * self.period)
        interval_out_period = interval - \
            interval_in_period * DAYS_PER_WEEK * self.period
        return base, interval_in_period, interval_out_period

    def _get_info_month(self, date):
        base = MONTHS_PER_YEAR
        interval = date.month - self.start_date.month + \
            MONTHS_PER_YEAR * (date.year - self.start_date.year) - \
            (date.day < self.start_date.day)
        interval_in_period = interval // self.period
        stop_year = self.start_date.year + \
            (self.start_date.month + interval_in_period > MONTHS_PER_YEAR)
        stop_month = (self.start_date.month +
                      interval_in_period * self.period) % MONTHS_PER_YEAR
        stop_month_range = monthrange(stop_year, stop_month)[1]
        if self.start_date.day < stop_month_range:
            stop_day = self.start_date.day
        else:
            stop_day = stop_month_range
        interval_out_period = (
            date - datetime(stop_year, stop_month, stop_day).date()).days
        return base, interval_in_period, interval_out_period


class Withdraw(models.Model):
    amount = models.IntegerField(_('amount'))
    date = models.DateField(_('withdrawn on'), auto_now_add=True)
    is_open = models.BooleanField(_('is open'), default=True, db_index=True)

    class Meta:
        verbose_name = _('Withdraw')
        verbose_name_plural = _('Withdraws')

    def __str__(self):
        return "{obj.amount} on {obj.date}".format(obj=self)


@receiver(models.signals.post_save, sender=Passbook,
          dispatch_uid='update_withdraw')
def update_withdraw(sender, instance, created, **kwargs):
    if created and instance.is_open:
        Withdraw.objects.filter(is_open=True).update(is_open=False)
