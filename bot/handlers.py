"""
Telegram bot logic.
"""
import logging

from telegram.ext import CommandHandler, MessageHandler, Filters

from bot.utils import user_and_group
from expenses.models import Expense


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

HANDLERS = [
]


@user_and_group
def start(update, context, user, group):
    logging.info('[ /start ]: %s', update)
    logging.info('[ /start ]: user: %s', user)
    logging.info('[ /start ]: grop: %s', group)

    context.bot.send_message(chat_id=update.message.chat_id, text="Hola {}!".format(user))

HANDLERS.append(CommandHandler('start', start))


def echo(update, context):
    logging.info('[ echo ]: %s', update)
    context.bot.send_message(chat_id=update.message.chat_id, text=update.message.text)

HANDLERS.append(MessageHandler(Filters.text, echo))


@user_and_group
def load_expense(update, context, user, group):
    if not context.args:
        text = 'Necesito que me digas cuanto pagaste y una descripción del gasto.'
        context.bot.send_message(chat_id=update.message.chat_id, text=text)
        return

    amount, *description = context.args

    try:
        amount = amount.replace(',', '.')
        amount = float(amount)

    except ValueError:
        text = 'El primer valor que me pasas después del comando tiene que ser el valor de '\
               'lo que pagaste, "{}" no es un número válido.'.format(context.args[0])
        context.bot.send_message(chat_id=update.message.chat_id, text=text)
        return
    if not description:
        text = 'Necesito que agregues una descripción del gasto.'
        context.bot.send_message(chat_id=update.message.chat_id, text=text)
        return

    description = ' '.join(description)
    expense = Expense(user=user, group=group, description=description, amount=amount)
    expense.save()
    text = 'se guardo tu gasto {}'.format(expense)
    context.bot.send_message(chat_id=update.message.chat_id, text=text)

HANDLERS.append(CommandHandler('gasto', load_expense))


def unknown(update, context):
    text = "Perdón, ese comando no lo entiendo."
    context.bot.send_message(chat_id=update.message.chat_id, text=text)

HANDLERS.append(MessageHandler(Filters.command, unknown))
