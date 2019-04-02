from django.contrib import admin

from expenses.models import Expense, Tag, Division


admin.site.register(Expense)
admin.site.register(Tag)
admin.site.register(Division)
