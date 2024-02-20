"""
ASGI config for room_402 project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter, ChannelNameRouter
from django.core.asgi import get_asgi_application
from django.urls import path
from message import consumer
from message.consumer import message_consumer

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'room_402.settings')

application = ProtocolTypeRouter({
    'http': get_asgi_application,
    'websocket': AuthMiddlewareStack(
        URLRouter([
            path('ws/<str:user_id>', consumer.message_consumer.as_asgi()),
        ])
    ),
    'channel_layer': ChannelNameRouter({
        'notify_user': message_consumer,
    }),
})
