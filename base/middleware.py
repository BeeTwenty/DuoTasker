from zoneinfo import ZoneInfo

from django.db import OperationalError, ProgrammingError
from django.shortcuts import redirect
from django.utils import timezone, translation

from .models import SiteConfiguration


class SiteSetupAndLocaleMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path
        exempt_paths = (
            '/setup/',
            '/i18n/',
            '/admin/',
            '/static/',
            '/favicon.ico',
            '/manifest.json',
        )

        configuration = None
        try:
            configuration = SiteConfiguration.objects.first()
        except (OperationalError, ProgrammingError):
            configuration = None

        if not any(path.startswith(prefix) for prefix in exempt_paths):
            if configuration is None or not configuration.setup_complete:
                return redirect('setup')

        if configuration is not None:
            language_code = request.session.get('django_language') or configuration.default_language or 'en'
            translation.activate(language_code)
            request.LANGUAGE_CODE = language_code

            timezone_name = configuration.default_timezone or 'UTC'
            try:
                timezone.activate(ZoneInfo(timezone_name))
            except Exception:
                timezone.activate(ZoneInfo('UTC'))

        response = self.get_response(request)
        return response