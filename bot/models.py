from django.db import models


class TelegramUser(models.Model):
    """
    Extend django user with telegram user data.
    """
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE, related_name='telegram')
    chat_id = models.IntegerField()
    username = models.CharField(max_length=256, blank=True)
