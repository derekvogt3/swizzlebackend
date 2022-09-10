# chat/consumers.py
import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from events.models import Event
from chat.models import ChatMessage
from .serializers import ChatMessageSerializer
from chat import serializers
from uuid import UUID
from json import JSONEncoder


old_default = JSONEncoder.default


def new_default(self, obj):
    if isinstance(obj, UUID):
        return str(obj)
    return old_default(self, obj)


JSONEncoder.default = new_default


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.event_id = self.scope['url_route']['kwargs']['event_id']
        self.room_group_name = 'chat_%s' % self.event_id

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        print(text_data)
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        user = self.scope['user']
        event = Event.objects.get(
            id=self.scope['url_route']['kwargs']['event_id'])

        data = {'user': user.id, 'event': event.id, 'message_text': message}
        serializer = ChatMessageSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            response = serializer.data
        else:
            response = serializer.errors

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': json.dumps(response)
            }
        )

    # Receive message from room group
    def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message
        }))
