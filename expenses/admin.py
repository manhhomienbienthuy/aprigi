from django.contrib import admin

from .models import Expense, Income


class IncomeAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'amount', 'date', )
    list_filter = ['amount', 'date', ]


class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'amount', 'date', 'purpose', )
    list_filter = ['amount', 'date', ]


admin.site.register(Income, IncomeAdmin)
admin.site.register(Expense, ExpenseAdmin)
