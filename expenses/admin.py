from django.contrib import admin

from expenses.models import Expense, Tag, Division, ExchangeRate


admin.site.register(Tag)
admin.site.register(Division)


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('date', 'amount', 'group', 'description')


@admin.register(ExchangeRate)
class ExchangeRateAdmin(admin.ModelAdmin):
    list_display = ('date', 'currency', 'rate')
