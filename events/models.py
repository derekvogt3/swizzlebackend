from django.db import models
import uuid
from firebase_auth.models import MyUser


# Create your models here.


class Event(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=128)
    users = models.ManyToManyField(MyUser, through='Invitations')
    created_at = models.DateTimeField(auto_now_add=True)
    admin_id = models.CharField(max_length=36)
    event_settings = models.TextField()
    location_name = models.CharField(max_length=128)
    location_lat = models.IntegerField()
    location_lng = models.IntegerField()
    number_of_attendees = models.IntegerField()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['created_at']


class Invitations(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    status = models.CharField(default='invited', max_length=100)
    invite_idx = models.IntegerField()
    date_joined = models.DateField()
