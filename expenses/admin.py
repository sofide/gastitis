from django.contrib import admin

from expenses.models import Expense, Category, Division


admin.site.register(Expense)
admin.site.register(Category)
admin.site.register(Division)
