from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help='Displays Hello.'

    def handle(self,*args,**kawargs):
        self.stdout.write('Hello World')