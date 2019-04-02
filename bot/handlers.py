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

    context.bot.send_message(chat_id=update.message.chat_id, text="Hi {}".format(user))
    context.bot.send_message(chat_id=update.message.chat_id, text="I'm a bot, please talk to me!")


HANDLERS.append(CommandHandler('start', start))

def echo(update, context):
    logging.info('[ echo ]: %s', update)
    context.bot.send_message(chat_id=update.message.chat_id, text=update.message.text)

HANDLERS.append(MessageHandler(Filters.text, echo))


def caps(update, context):
    text_caps = ' '.join(context.args).upper()
    context.bot.send_message(chat_id=update.message.chat_id, text=text_caps)

HANDLERS.append(CommandHandler('caps', caps))


@user_and_group
def load_expense(update, context, user, group):
    if not context.args:
        context.bot.send_message(chat_id=update.message.chat_id, text='dame precio y desc')
        return

    amount, *description = context.args

    try:
        amount = float(context.args[0])

    except ValueError:
        text = 'First argument must be a  number, and {} is not a number'.format(
            context.args[0],
        )
        context.bot.send_message(chat_id=update.message.chat_id, text=text)
        return
    if not description:
        context.bot.send_message(chat_id=update.message.chat_id, text='dame desc')
        return

    description = ' '.join(description)
    expense = Expense(user=user, group=group, description=description, amount=amount)
    expense.save()
    text = 'se guardo tu gasto {}'.format(expense)
    context.bot.send_message(chat_id=update.message.chat_id, text=text)



HANDLERS.append(CommandHandler('cargar', load_expense))




def unknown(update, context):
    context.bot.send_message(chat_id=update.message.chat_id, text="Sorry, I didn't understand that command.")

HANDLERS.append(MessageHandler(Filters.command, unknown))
