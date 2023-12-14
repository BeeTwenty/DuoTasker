from django.apps import AppConfig
from django.contrib.auth import get_user_model
from django.db.utils import OperationalError
import os


class BaseConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'base'

    def ready(self):
        try:
            User = get_user_model()
            if not User.objects.filter(is_superuser=True).exists():
                User.objects.create_superuser(
                    os.getenv('DJANGO_SUPERUSER_USERNAME'),
                    os.getenv('DJANGO_SUPERUSER_EMAIL'),
                    os.getenv('DJANGO_SUPERUSER_PASSWORD')
                )
        except OperationalError:
            pass  # This is fine, happens when the db isn't ready yet
