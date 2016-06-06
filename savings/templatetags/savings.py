from django import template
from django.utils import dateparse

register = template.Library()


@register.filter
def interest_on_withdraw(obj, date):
    return obj.interest_on_withdraw(dateparse.parse_date(date))
