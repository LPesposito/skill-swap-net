import json
import re

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer


class ChatConsumer(WebsocketConsumer):
    """Basic WebSocket consumer for chat using Django Channels.

    - connect: extracts room name from the URL path, joins group and accepts
    - disconnect: leaves the group
    - receive: expects JSON with a `message` key, forwards it to the group
    - chat_message: handler invoked for group messages to send JSON to socket
    """

    def connect(self):
        # Try to extract room name from the scope's path or url_route kwargs
        scope = getattr(self, "scope", {})
        room = None
        # Prefer url_route kwargs if available (when you use routing with a regex)
        url_kwargs = scope.get("url_route", {}).get("kwargs", {})
        if url_kwargs and "room_name" in url_kwargs:
            room = url_kwargs["room_name"]

        if not room:
            # Fallback: parse last path segment
            path = scope.get("path", "")
            m = re.search(r"/([^/]+)/?$", path)
            room = m.group(1) if m else "global"

        self.room_name = room
        self.group_name = f"chat_{self.room_name}"

        # Join room group
        async_to_sync(self.channel_layer.group_add)(self.group_name, self.channel_name)

        # Accept the connection
        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(self.group_name, self.channel_name)

    def receive(self, text_data=None, bytes_data=None):
        # Accept JSON payloads with a `message` field; gracefully handle plain text
        try:
            data = json.loads(text_data) if text_data else {}
        except Exception:
            data = {"message": text_data}

        message = data.get("message")
        if message is None:
            # nothing to do
            return

        sender = None
        user = self.scope.get("user")
        if user and getattr(user, "is_authenticated", False):
            try:
                sender = str(user.username)
            except Exception:
                sender = str(user)
        else:
            sender = data.get("sender", "anonymous")

        # Broadcast message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.group_name,
            {
                "type": "chat.message",
                "message": message,
                "sender": sender,
            },
        )

    def chat_message(self, event):
        # Receive message from group
        payload = {"message": event.get("message"), "sender": event.get("sender")}
        self.send(text_data=json.dumps(payload))
