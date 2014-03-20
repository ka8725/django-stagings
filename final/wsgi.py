"""
WSGI config for final project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/howto/deployment/wsgi/
"""

import os
from configurations.wsgi import get_wsgi_application
from dj_static import Cling

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'final.settings')
os.environ.setdefault('DJANGO_CONFIGURATION', 'Prod')
application = Cling(get_wsgi_application())
