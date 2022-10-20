#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

from dotenv import load_dotenv

load_dotenv()

def main():
    """Run administrative tasks."""

    pwd = os.getcwd()
    paths = [
        pwd,
        os.path.join(pwd, 'apps')
    ]

    for index, path in enumerate(paths):
        if path not in sys.path:
            sys.path.insert(index, path)

    if os.environ['DEBUG'] == '1':
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')
    else:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.production')

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
