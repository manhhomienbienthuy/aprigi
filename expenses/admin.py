from django.contrib import admin

from .models import Balance


class BalanceAdmin(admin.ModelAdmin):
    list_display = ('amount', 'kind', 'date', 'notes', )
    list_filter = ['kind', 'date', ]


admin.site.register(Balance, BalanceAdmin)
