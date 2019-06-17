"""
Telegram bot logic.
"""
import logging

from telegram.ext import CommandHandler, MessageHandler, Filters
from telegram import ParseMode

from bot.utils import (
    get_month_expenses,
    get_month_and_year,
    is_group,
    new_expense,
    new_payment,
    show_expenses,
    user_and_group,
)
from expenses.models import Expense


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)


@user_and_group
def start(update, context, user, group):
    logging.info('[ /start ]: %s', update)
    text = "Hola {}!\n\n".format(user)
    text += "Este es un proyecto de juguete. Es para uso personal, y todavía se encuentra " \
            "desarrollo. No se ofrecen garantías de seguridad ni de privacidad. Usalo bajo tu " \
            "propio riesgo.\n\n"
    text += "Si no sabés qué hacer a continuación, /help\n\n"
    text += "This is a toy project, it's for personal use and it is still under " \
            "development. There aren't any warranties of security or privacy. Use it under " \
            "your own risk.\n\n"
    text += "If you don't know how to use this bot, just ask for /help\n\n"
    context.bot.send_message(chat_id=update.message.chat_id, text=text)


def show_help(update, context):
    help_text = [
        'Para registrar un gasto `/gasto {monto} {descripcion} (dd {fecha} tt {tag1,tag2,tag3})`',
        'Para mostrar el total hasta el momento `/total`',
        'Para mostrar el total de un mes `/mes ({mes}) ({año})`',
    ]
    text = '\n\n'.join(help_text)
    context.bot.send_message(chat_id=update.message.chat_id, text=text,
                             parse_mode=ParseMode.MARKDOWN)


@user_and_group
def load_expense(update, context, user, group):
    text = new_expense(context.args, user, group)
    context.bot.send_message(chat_id=update.message.chat_id, text=text)


@user_and_group
def load_payment(update, context, user, group):
    text = new_payment(context.args, update, user, group)
    context.bot.send_message(chat_id=update.message.chat_id, text=text)


@user_and_group
def total_expenses(update, context, user, group):
    text = show_expenses(group)
    context.bot.send_message(chat_id=update.message.chat_id, text=text)


@user_and_group
def month_expenses(update, context, user, group):
    month, year = get_month_and_year(context.args)
    text = get_month_expenses(group, year, month)
    context.bot.send_message(chat_id=update.message.chat_id, text=text)


def unknown(update, context):
    text = "Perdón, ese comando no lo entiendo. Si no sabés que hacer, /help."
    context.bot.send_message(chat_id=update.message.chat_id, text=text)


# Register your handlers here
HANDLERS = [
    CommandHandler('start', start),
    CommandHandler('help', show_help),
    CommandHandler('gasto', load_expense),
    CommandHandler('g', load_expense),
    CommandHandler('pago', load_payment),
    CommandHandler('p', load_payment),
    CommandHandler('total', total_expenses),
    CommandHandler('mes', month_expenses),
    CommandHandler('month', month_expenses),
    CommandHandler('m', month_expenses),
    MessageHandler(Filters.command, unknown),
]
