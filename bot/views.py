import json

from django.conf import settings
from django.http import Http404, HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt


from bot.bot import Bot


@csrf_exempt
def webhook(request, token):
    if not token == settings.BOT_TOKEN:
        raise Http404()
    bot = Bot()
    bot.webhook(json.loads(request.body.decode('utf-8')))
