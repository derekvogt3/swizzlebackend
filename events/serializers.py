from rest_framework import serializers
from .models import Event


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['id', 'name', 'admin_id', 'event_settings', 'location_name',
                  'location_lat', 'location_lng', 'number_of_attendees']
