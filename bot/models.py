from django.db import models
import uuid

class TelegramUser(models.Model):
    """
    Extend django user with telegram user data.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False )
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE, related_name='telegram')
    chat_id = models.IntegerField()
    username = models.CharField(max_length=256, blank=True)

    def __str__(self):
        return self.username

class TelegramGroup(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False )
    users = models.ManyToManyField('auth.User', related_name='telegram_groups')
    chat_id = models.IntegerField()
    name = models.CharField(max_length=256)

    def __str__(self):
        return self.name
