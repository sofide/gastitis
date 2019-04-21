"""
Telegram bot logic.
"""
import logging

from telegram.ext import CommandHandler, MessageHandler, Filters

from bot.utils import user_and_group, new_expense, show_expenses
from expenses.models import Expense


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

HANDLERS = [
]


@user_and_group
def start(update, context, user, group):
    logging.info('[ /start ]: %s', update)
    text = "Hola {}!".format(user)
    text += "\n\nEste es un proyecto de juguete. Es para uso personal, y todavía se encuentra " \
            "desarrollo. No se ofrecen garantías de seguridad ni de privacidad. Usalo bajo tu " \
            "propio riesgo."
    text += "\n\nThis is a toy project, it's for personal use and it is still in development. " \
            "There isn't any waranty of security or privacy. Use it under your own risk."
    context.bot.send_message(chat_id=update.message.chat_id, text=text)


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
HANDLERS.append(CommandHandler('g', load_expense))


@user_and_group
def total_expenses(update, context, user, group):
    text = show_expenses(group)
    context.bot.send_message(chat_id=update.message.chat_id, text=text)

HANDLERS.append(CommandHandler('total', total_expenses))


def unknown(update, context):
    text = "Perdón, ese comando no lo entiendo."
    context.bot.send_message(chat_id=update.message.chat_id, text=text)

HANDLERS.append(MessageHandler(Filters.command, unknown))
