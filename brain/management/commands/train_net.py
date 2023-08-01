from django.core.management.base import BaseCommand, CommandError
from brain.models import ClassifierConfig


class Command(BaseCommand):
    help = ''

    # def add_arguments(self, parser):
    #     parser.add_argument('foo', nargs='+', type=int)

    def handle(self, *args, **options):
        for config in ClassifierConfig.objects.all():
            config.train()
