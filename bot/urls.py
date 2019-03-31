from django.contrib import admin
from django.urls import path, include

from bot.views import webhook

urlpatterns = [
    path('<token>/', webhook),
]
