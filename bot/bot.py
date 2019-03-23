"""
Telegram bot logic.
"""
import logging

from django.conf import settings
from django.contrib.auth.models import User
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

from bot.models import TelegramUser
from expenses.models import Expense


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

def get_user(update):
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

    return user


updater = Updater(token=settings.BOT_TOKEN, use_context=True)

dispatcher = updater.dispatcher

def start(update, context):
    logging.info('blabla')
    logging.info('update: %s', update)

    user = get_user(update)
    context.bot.send_message(chat_id=update.message.chat_id, text="Hi {}".format(user))
    context.bot.send_message(chat_id=update.message.chat_id, text="I'm a bot, please talk to me!")


start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

def echo(update, context):
    context.bot.send_message(chat_id=update.message.chat_id, text=update.message.text)

echo_handler = MessageHandler(Filters.text, echo)
dispatcher.add_handler(echo_handler)


def caps(update, context):
    text_caps = ' '.join(context.args).upper()
    context.bot.send_message(chat_id=update.message.chat_id, text=text_caps)

caps_handler = CommandHandler('caps', caps)
dispatcher.add_handler(caps_handler)

def load_expense(update, context):
    user = get_user(update)
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



expense_handler = CommandHandler('cargar', load_expense)
dispatcher.add_handler(expense_handler)




def unknown(update, context):
    context.bot.send_message(chat_id=update.message.chat_id, text="Sorry, I didn't understand that command.")

unknown_handler = MessageHandler(Filters.command, unknown)
dispatcher.add_handler(unknown_handler)
