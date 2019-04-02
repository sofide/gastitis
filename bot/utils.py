from django.contrib.auth.models import User

from bot.models import TelegramUser, TelegramGroup


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
    group_name = group_data.title or username + '__private'

    group, _ = TelegramGroup.objects.get_or_create(chat_id=group_id, defaults={
        'name': group_name,
    })
    group.users.add(user)


    return user, group



