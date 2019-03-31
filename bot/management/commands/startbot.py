from django.core.management.base import BaseCommand

from bot.bot import Bot


class Command(BaseCommand):
    help = 'Start testing bot.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Vamos a arrancar con el bot'))
        Bot()
