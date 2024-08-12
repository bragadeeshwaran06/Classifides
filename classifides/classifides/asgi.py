import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application
from django.urls import re_path

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "classifides.settings")  # Update with your actual settings module name
django_asgi_app = get_asgi_application()

from chat.consumers import AdChatConsumer

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter([
                re_path(r'^ws/ads/(?P<ad_id>\d+)/$', AdChatConsumer.as_asgi()),  # Correct usage of re_path
            ])
        )
    ),
})
