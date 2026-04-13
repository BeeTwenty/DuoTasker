from django.apps import AppConfig


class PwaConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.pwa"
    label = "duotasker_pwa"
    verbose_name = "DuoTasker PWA"
