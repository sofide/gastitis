from django.db import models

from bot.models import TelegramGroup


# Define accepted currency. Keys must have one character long.
CURRENCY = {
    'u': 'usd',
    'y': 'yen',
}


class Tag(models.Model):
    """
    Expenses tag, to keep track grouped expensives, and compare them in different periods.
    """
    name = models.CharField(max_length=256)
    group = models.ForeignKey(TelegramGroup, on_delete=models.CASCADE, related_name='tags')

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class ExchangeRate(models.Model):
    """
    Exchange rates for currencies different from default.
    """
    currency = models.CharField(max_length=1, choices=CURRENCY.items())
    rate = models.DecimalField(decimal_places=4, max_digits=10)
    date = models.DateField()


class Expense(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='expenses')
    group = models.ForeignKey(TelegramGroup, on_delete=models.CASCADE, related_name='expenses')
    description = models.TextField()
    amount = models.DecimalField(decimal_places=2, max_digits=256)
    tags = models.ManyToManyField(Tag, related_name='expenses')
    date = models.DateField()
    created_date = models.DateTimeField(auto_now=True)

    # fields that represent an expense in a currency different from default.
    original_currency = models.CharField(max_length=1, choices=CURRENCY.items(), null=True)
    original_amount = models.DecimalField(decimal_places=2, max_digits=256, null=True)

    class Meta:
        ordering = ['-date', 'amount']

    def __str__(self):
        return '{} - ${} - {}'.format(self.date, self.amount, self.description)


class Division(models.Model):
    """
    How much should everyone pay to afford the total expenses.
    """
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    portion = models.FloatField()

    def __str__(self):
        return '{} - %{}'.format(self.user, self.portion)
