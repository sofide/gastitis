from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = 'Start testing bot.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Vamos a arrancar con el bot'))
        from bot.bot import updater
        updater.start_polling()
