import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from django.contrib.auth import get_user_model
from django.db.models import Q

from chat.models import Message, Conversation
from chat.utils import date_or_time, messages_to_json, message_to_json
from chat.views import redis_instance

User = get_user_model()


class ChatConsumer(WebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.conversation = None
        self.conversation_created = None
        self.room_group_name = None

    def get_messages(self, data):
        messages = sorted(self.conversation.messages.all(), reverse=True, key=lambda x: x.timestamp)
        content = {
            "command": "messages",
            "messages": messages_to_json(messages)
        }
        self.send(text_data=json.dumps({'message': content}))

    def new_message(self, data):
        friend_is_in_chat = redis_instance.exists(f"{self.room_group_name}_{data['to_user_id']}")
        message = Message.objects.create(conversation=self.conversation, from_user_id=data["from_user_id"],
                                         to_user_id=data["to_user_id"], content=data["message"], read=friend_is_in_chat)
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, {"type": "chat_message", "message": message_to_json(message)}
        )

    def read(self, data):
        if not self.conversation_created:
            Message.objects.filter(
                Q(conversation_id=self.conversation.id) & Q(to_user_id=self.scope["user"].id) & Q(read=False)).update(read=True)
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {"type": "chat_message", "message": {"command": "read", "reader_pk": self.scope["user"].pk}}
            )

    def user_typing(self, data):
        if data["state"] == "start":
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {"type": "chat_message", "message": {"command": "user_typing", "state": "typing...", "from_user_pk": self.scope["user"].pk}}
            )
        elif data["state"] == "stop":
            user_status = redis_instance.get(self.scope["user"].pk).decode('utf-8')
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {"type": "chat_message", "message": {"command": "user_typing", "state": user_status, "from_user_pk": self.scope["user"].pk}}
            )

    commands = {
        "get_messages": get_messages,
        "new_message": new_message,
        "read": read,
        "user_typing": user_typing,
    }

    def connect(self):
        self.room_group_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.conversation, self.conversation_created = Conversation.objects.get_or_create(name=self.room_group_name)
        redis_instance.set(f"{self.room_group_name}_{self.scope['user'].pk}", '')

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        if self.conversation.messages.exists() and self.conversation_created:
            self.scope["user"].friends.add(self.conversation.messages.first().to_user_id)
        elif not self.conversation.messages.exists():
            self.conversation.delete()

        redis_instance.delete(f"{self.room_group_name}_{self.scope['user'].pk}")

        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        self.commands[text_data_json["action"]](self, text_data_json)

    def chat_message(self, event):
        message = event["message"]
        self.send(text_data=json.dumps({"message": message}))


class UserStatusConsumer(WebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.room_group_name = "userstatus"

    def connect(self):
        redis_instance.set(self.scope["user"].pk, "Online")

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        redis_instance.delete(self.scope["user"].pk)

        user_status = {
            "user_pk": self.scope["user"].pk,
            "status": "Offline",
        }

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, {"type": "chat_message", "user_status": user_status}
        )

        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        user_status = {
            "user_pk": self.scope["user"].pk,
            "status": text_data_json["status"],
        }

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, {"type": "chat_message", "user_status": user_status}
        )

    def chat_message(self, event):
        user_status = event["user_status"]
        self.send(text_data=json.dumps({"user_status": user_status}))


class NotificationConsumer(WebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.room_group_name = None

    def connect(self):
        self.room_group_name = self.scope["url_route"]["kwargs"]["username"]
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        username = User.objects.get(pk=text_data_json["to_user_id"]).username
        async_to_sync(self.channel_layer.group_send)(
            username, {"type": "send_notification", "from": self.scope["user"].username}
        )

    def send_notification(self, event):
        message = event["from"]
        self.send(text_data=json.dumps({"from": message}))
