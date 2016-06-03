from django.contrib import admin

from .models import Passbook


class PassbookAdmin(admin.ModelAdmin):
    list_display = ('number', 'account_number', 'amount', 'period', 'rate',
                    'start_date', 'stop_date', 'is_open', 'interest', )
    list_filter = ['is_open', 'period', 'start_date', 'stop_date', ]


admin.site.register(Passbook, PassbookAdmin)
