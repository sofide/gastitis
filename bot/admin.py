from django.contrib import admin

from bot.models import TelegramGroup, TelegramUser

# Register your models here.
admin.site.register(TelegramGroup)
admin.site.register(TelegramUser)
