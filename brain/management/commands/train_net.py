from django.core.management.base import BaseCommand, CommandError
from brain.net import VisitorClassifier


class Command(BaseCommand):
    help = ''

    # def add_arguments(self, parser):
    #     parser.add_argument('foo', nargs='+', type=int)

    def handle(self, *args, **options):
        vc = VisitorClassifier(load=False, train=True)
        vc.save()
