"""
Initialize telegram bot and start polling messages.
"""

from django.conf import settings
from telegram.ext import Application

from bot.handlers import HANDLERS


class Bot:
    def __init__(self, token=settings.BOT_TOKEN):
        self.application = Application.builder().token(token).build()

        for handler in HANDLERS:
            self.application.add_handler(handler)

        self.application.run_polling()
