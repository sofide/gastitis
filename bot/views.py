import json

from django.conf import settings
from django.http import Http404, HttpResponse
from django.shortcuts import render

from bot.bot import Bot


def webhook(request, token):
    if not token == settings.BOT_TOKEN:
        raise Http404()
    bot = Bot()
    bot.webhook(json.loads(request.body.decode('utf-8')))
