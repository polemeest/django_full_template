"""
ASGI config for simple project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os
# import sys
# from pathlib import Path
from config.settings import BASE_DIR
from django.core.asgi import get_asgi_application
from utils.middleware import TokenAuthMiddleware

# This allows easy placement of apps within the interior

# ROOT_DIR = Path(__file__).resolve(strict=True).parent
# sys.path.append(str(ROOT_DIR / "src"))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", os.path.join(BASE_DIR, "config.settings"))

# Import websocket application here, so apps from django_application are loaded first
from config.routing import websocket_urlpatterns  # noqa isort:skip
from channels.routing import ProtocolTypeRouter, URLRouter  # noqa isort:skip

application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        "websocket": TokenAuthMiddleware(URLRouter(websocket_urlpatterns)),
    }
)
