"""
WSGI config for homepage project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/wsgi/
"""

import os
import sys
from pathlib import Path

from django.core.wsgi import get_wsgi_application

BASE_DIR = Path(__file__).resolve().parent.parent
for path in (BASE_DIR, BASE_DIR / 'apps'):
    path = str(path)
    if path not in sys.path:
        sys.path.insert(0, path)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.production')

application = get_wsgi_application()
