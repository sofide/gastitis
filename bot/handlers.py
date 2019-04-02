"""
Telegram bot logic.
"""
import logging

from django.contrib.auth.models import User
from telegram.ext import CommandHandler, MessageHandler, Filters

from bot.models import TelegramUser, TelegramGroup
from expenses.models import Expense


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

HANDLERS = [
]

def get_user_and_group(update):
    user_data = update.message.from_user
    chat_id = user_data.id
    first_name = getattr(user_data, 'first_name', chat_id)
    last_name = getattr(user_data, 'last_name', '')
    telegram_username = getattr(user_data, 'username', '')
    username = telegram_username or first_name
    user, _ = User.objects.get_or_create(telegram__chat_id=user_data.id, defaults={
        'username': username,
        'first_name': first_name,
    })

    TelegramUser.objects.update_or_create(
        user=user, chat_id=chat_id, defaults={
            'username': telegram_username
        })
    group_data = update.message.chat
    group_id = group_data.id
    group_name = group_data.title

    group, _ = TelegramGroup.objects.get_or_create(chat_id=group_id, defaults={
        'name': group_name,
    })
    group.users.add(user)


    return user, group



def start(update, context):
    logging.info('[ /start ]: %s', update)

    user, group = get_user_and_group(update)
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

def load_expense(update, context):
    user, group = get_user_and_group(update)
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
    expense = Expense(user=user, description=description, amount=amount)
    expense.save()
    text = 'se guardo tu gasto {}'.format(expense)
    context.bot.send_message(chat_id=update.message.chat_id, text=text)



HANDLERS.append(CommandHandler('cargar', load_expense))




def unknown(update, context):
    context.bot.send_message(chat_id=update.message.chat_id, text="Sorry, I didn't understand that command.")

HANDLERS.append(MessageHandler(Filters.command, unknown))
