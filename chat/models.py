import uuid
from django.db import models
from events.models import Event
from firebase_auth.models import MyUser

# Create your models here.


class ChatMessage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    event = models.ForeignKey(
        Event, on_delete=models.CASCADE, related_name='chat_messages')
    created_at = models.DateTimeField(auto_now_add=True)
    message_text = models.TextField(blank=False)
