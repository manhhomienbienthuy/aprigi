from django.contrib import admin

from .models import Objective, Passbook, Withdraw


class PassbookAdmin(admin.ModelAdmin):
    list_display = ('number', 'account_number', 'amount', 'period', 'rate',
                    'start_date', 'stop_date', 'is_open', 'interest', )
    list_filter = ['is_open', 'period', 'start_date', 'stop_date', ]


class WithdrawAdmin(admin.ModelAdmin):
    list_display = ('amount', 'is_open', 'date', )
    list_filter = ['is_open', ]


class ObjectiveAdmin(admin.ModelAdmin):
    list_display = ('year', 'amount', )
    list_filter = ['year', ]


admin.site.register(Passbook, PassbookAdmin)
admin.site.register(Withdraw, WithdrawAdmin)
admin.site.register(Objective, ObjectiveAdmin)
