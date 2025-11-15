"""
ASGI config for SkillSwapProject project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SkillSwapProject.settings')

# Use Channels ProtocolTypeRouter to route HTTP to Django and WebSocket to
# our consumers. We import routing from the communication app.
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
import communication.routing

application = ProtocolTypeRouter(
	{
		"http": get_asgi_application(),
		"websocket": AuthMiddlewareStack(URLRouter(communication.routing.websocket_urlpatterns)),
	}
)
