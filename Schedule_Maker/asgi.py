"""
ASGI config for Schedule_Maker project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""
# PYTHON IMPORTS
import os
# DJANGO IMPORTS
from django.core.asgi import get_asgi_application


os.environ.setdefault(
    'DJANGO_SETTINGS_MODULE', 'Schedule_Maker.settings'
)

application = get_asgi_application()
