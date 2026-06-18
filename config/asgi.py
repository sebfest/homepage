"""
ASGI config for homepage project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""

import os
import sys
from pathlib import Path

from django.core.asgi import get_asgi_application

BASE_DIR = Path(__file__).resolve().parent.parent
for path in (BASE_DIR, BASE_DIR / 'apps'):
    path = str(path)
    if path not in sys.path:
        sys.path.insert(0, path)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.production')

application = get_asgi_application()
