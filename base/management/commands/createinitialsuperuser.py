from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
import os

class Command(BaseCommand):
    help = 'Create a superuser if one does not exist'

    def handle(self, *args, **kwargs):
        User = get_user_model()
        if not User.objects.filter(is_superuser=True).exists():
            username = os.getenv('DJANGO_SUPERUSER_USERNAME')
            email = os.getenv('DJANGO_SUPERUSER_EMAIL')
            password = os.getenv('DJANGO_SUPERUSER_PASSWORD')
            if username and email and password:
                User.objects.create_superuser(username, email, password)
                self.stdout.write(self.style.SUCCESS('Successfully created superuser'))
            else:
                self.stdout.write(self.style.WARNING('Superuser details not provided in environment variables'))
