"""
WSGI config for Scheduling_Maker project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/wsgi/
"""
# PYTHON IMPORTS
import os
# DJANGO IMPORTS
from django.core.wsgi import get_wsgi_application


os.environ.setdefault(
    'DJANGO_SETTINGS_MODULE', 'Scheduling_Maker.settings'
)

application = get_wsgi_application()
