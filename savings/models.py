from calendar import monthrange
from datetime import datetime

from django.db import models
from django.utils.translation import ugettext_lazy as _


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
            return round(self.amount * self.rate / 100 / 365 * self.period * 7)
        return round(self.amount * self.rate / 100 / 12 * self.period)
    interest.short_description = _('interest (expected)')

    def interest_on_withdraw(self, date):
        if not self.is_open or self.period_type not in (self.WEEK, self.MONTH):
            return None
        rate_out_period = 0.6
        days_per_year = 365
        days_per_week = 7
        months_per_year = 12

        if self.period_type == self.WEEK:
            base = days_per_year / days_per_week
            interval = (date - self.start_date).days
            interval_in_period = interval // (days_per_week * self.period)
            interval_out_period = interval - \
                interval_in_period * days_per_week * self.period
        else:
            base = months_per_year
            interval = date.month - self.start_date.month + \
                months_per_year * (date.year - self.start_date.year) - \
                (date.day < self.start_date.day)
            interval_in_period = interval // self.period
            stop_year = self.start_date.year + \
                (self.start_date.month + interval_in_period > 12)
            stop_month = (self.start_date.month +
                          interval_in_period * self.period) % 12
            stop_month_range = monthrange(stop_year, stop_month)[1]
            if self.start_date.day < stop_month_range:
                stop_day = self.start_date.day
            else:
                stop_day = stop_month_range
            interval_out_period = (
                date - datetime(stop_year, stop_month, stop_day).date()).days
        total_after_period = self.amount * \
            (1 + self.rate / 100 / base * self.period) ** interval_in_period
        total = total_after_period * \
            (1 + rate_out_period / 100 / days_per_year) ** interval_out_period
        return round(total - self.amount)


class Withdraw(models.Model):
    amount = models.IntegerField(_('amount'))
    date = models.DateField(_('withdrawn on'), auto_now_add=True)
    is_open = models.BooleanField(_('is open'), default=True, db_index=True)

    class Meta:
        verbose_name = _('Withdraw')
        verbose_name_plural = _('Withdraws')

    def __str__(self):
        return "{obj.amount} on {obj.date}".format(obj=self)
