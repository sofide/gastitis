"""
Telegram bot logic.
"""
import logging

from telegram.ext import CommandHandler, MessageHandler, filters
from telegram.constants import ParseMode

from bot.help_texts import HELP_TEXT
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
from extra_features.asado import how_much_asado_message
from extra_features.vianda import ViandaMessage
from use_cases.export import ExportExpenses


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)


@user_and_group
async def start(update, context, user, group):
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
    await context.bot.send_message(chat_id=update.message.chat_id, text=text)


async def show_help(update, context):
    await context.bot.send_message(
        chat_id=update.message.chat_id,
        text=HELP_TEXT,
        parse_mode=ParseMode.MARKDOWN
    )


@user_and_group
async def load_expense(update, context, user, group):
    text = await new_expense(context.args, user, group)
    await context.bot.send_message(chat_id=update.message.chat_id, text=text)


@user_and_group
async def load_payment(update, context, user, group):
    text = await new_payment(context.args, update, user, group)
    await context.bot.send_message(chat_id=update.message.chat_id, text=text)


@user_and_group
async def total_expenses(update, context, user, group):
    text = await show_expenses(group)
    await context.bot.send_message(
        chat_id=update.message.chat_id, text=text, parse_mode=ParseMode.MARKDOWN
    )


@user_and_group
async def month_expenses(update, context, user, group):
    month, year = get_month_and_year(context.args)
    text = await get_month_expenses(group, year, month)
    await context.bot.send_message(
        chat_id=update.message.chat_id, text=text, parse_mode=ParseMode.MARKDOWN
    )

async def calc_asado(update, context):
    try:
        people = int(context.args[0])
        text = how_much_asado_message(people)
    except:
        text = "Hubo un problema. Recordá pasar la cantidad de personas como parámetro."

    await context.bot.send_message(chat_id=update.message.chat_id, text=text)


@user_and_group
async def export(update, context, user, group):
    exporter = ExportExpenses(user, group)

    text = await exporter.run()
    await context.bot.send_message(
        chat_id=update.message.chat_id, text=text, parse_mode=ParseMode.MARKDOWN
    )


async def vianda(update, context):
    vianda_message = ViandaMessage(*context.args)

    text = vianda_message.message()
    await context.bot.send_message(
        chat_id=update.message.chat_id, text=text, parse_mode=ParseMode.MARKDOWN
    )


async def unknown(update, context):
    text = "Perdón, ese comando no lo entiendo. Si no sabés que hacer, /help."
    await context.bot.send_message(chat_id=update.message.chat_id, text=text)


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
    CommandHandler('asado', calc_asado),
    CommandHandler('a', calc_asado),
    CommandHandler('exportar', export),
    CommandHandler('vianda', vianda),
    MessageHandler(filters.COMMAND, unknown),
]
