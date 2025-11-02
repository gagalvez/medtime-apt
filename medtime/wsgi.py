"""
WSGI config for medtime project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""

import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'medtime.settings')

application = get_wsgi_application()

try:
    from django.core.management import call_command
    call_command('migrate', interactive=False)
except Exception as e:
    print("Error al ejecutar migraciones automáticas:", e)

try:
    from django.contrib.auth import get_user_model
    User = get_user_model()
    if not User.objects.filter(username="admin").exists():
        User.objects.create_superuser(
            username="admin",
            email="admin@example.com",
            password="admin123"
        )
except Exception as e:
    print("Error al crear superusuario automáticamente:", e)
