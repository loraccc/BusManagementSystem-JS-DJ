from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.utils.crypto import get_random_string

class Command(BaseCommand):
    help = 'Generate random users'

    def add_arguments(self, parser):
        parser.add_argument('count', type=int, help='Indicates the number of users to be created')
        # Uncomment the lines below if you want to add more functionality
        # parser.add_argument('-p', '--prefix', type=str, help='Define a username prefix')
        # parser.add_argument('-s', '--superuser', action='store_true', help='Create a superuser account')

    def handle(self, *args, **kwargs):
        count = kwargs['count']
        for _ in range(count):
            username = get_random_string(length=8)
            email = f'{username}@example.com'
            password = 'password123'
            User.objects.create_user(username=username, email=email, password=password)
            self.stdout.write(self.style.SUCCESS(f'User {username} created'))

        self.stdout.write(self.style.SUCCESS(f'{count} users created successfully'))
