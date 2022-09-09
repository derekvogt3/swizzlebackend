# chat/consumers.py
import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from events.models import Event
from chat.models import ChatMessage
from .serializers import ChatMessageSerializer
from chat import serializers
from uuid import UUID


class UUIDEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, UUID):
            # if the obj is uuid, we simply return the value of uuid
            return obj.hex
        return json.JSONEncoder.default(self, obj)


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
                'message': json.dumps(response, cls=UUIDEncoder)
            }
        )

    # Receive message from room group
    def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message
        }))
