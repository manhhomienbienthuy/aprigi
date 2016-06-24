from django.contrib import admin

from .models import Balance


class BalanceAdmin(admin.ModelAdmin):
    list_display = ('amount', 'kind', 'date', 'notes')


admin.site.register(Balance, BalanceAdmin)
