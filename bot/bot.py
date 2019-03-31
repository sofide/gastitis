from django.conf import settings
from telegram import Bot as TelegramBot, Update
from telegram.ext import Dispatcher, Updater

from bot.handlers import HANDLERS


class Bot:
    def __init__(self, token=settings.BOT_TOKEN):
        self.bot = TelegramBot(token)
        self.dispatcher = None

        if settings.DEBUG:
            self.updater = Updater(token, use_context=True)
            self.dispatcher = self.updater.dispatcher
            self.updater.start_polling()

        else:
            self.bot.set_webhook('{}/{}/{}/'.format(settings.SITE_DOMAIN, 'bot', token))
            self.dispatcher = Dispatcher(self.bot, None, workers=0, use_context=True)

        for handler in HANDLERS:
            self.dispatcher.add_handler(handler)

    def webhook(self, update):
        self.dispatcher.process_update(Update.de_json(update, self.bot))
