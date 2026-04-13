#!/usr/bin/env python
"""Django administrative utility for v2 settings split."""
import os
import sys


def main() -> None:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Ensure dependencies are installed and the environment is activated."
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
