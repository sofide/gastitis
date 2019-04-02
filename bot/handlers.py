"""
Telegram bot logic.
"""
import logging

from telegram.ext import CommandHandler, MessageHandler, Filters

from bot.utils import user_and_group, new_expense
from expenses.models import Expense


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

HANDLERS = [
]


@user_and_group
def start(update, context, user, group):
    logging.info('[ /start ]: %s', update)
    context.bot.send_message(chat_id=update.message.chat_id, text="Hola {}!".format(user))

HANDLERS.append(CommandHandler('start', start))


def echo(update, context):
    logging.info('[ echo ]: %s', update)
    context.bot.send_message(chat_id=update.message.chat_id, text=update.message.text)

HANDLERS.append(MessageHandler(Filters.text, echo))


@user_and_group
def load_expense(update, context, user, group):
    text = new_expense(context.args, user, group)
    context.bot.send_message(chat_id=update.message.chat_id, text=text)

HANDLERS.append(CommandHandler('gasto', load_expense))


def unknown(update, context):
    text = "Perdón, ese comando no lo entiendo."
    context.bot.send_message(chat_id=update.message.chat_id, text=text)

HANDLERS.append(MessageHandler(Filters.command, unknown))
