from django.db import models


class TelegramUser(models.Model):
    """
    Extend django user with telegram user data.
    """
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE, related_name='telegram')
    chat_id = models.IntegerField()
    username = models.CharField(max_length=256, blank=True)


class TelegramGroup(models.Model):
    users = models.ManyToManyField('auth.User', related_name='telegram_groups')
    chat_id = models.IntegerField()
    name = models.CharField(max_length=256)

    def __str__(self):
        return self.name
