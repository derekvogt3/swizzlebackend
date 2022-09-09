from rest_framework import serializers
from .models import Event, Invitation
from firebase_auth.serializers import MyUserSerializer


class InvitationSerializer(serializers.ModelSerializer):

    user = MyUserSerializer()

    class Meta:
        model = Invitation
        fields = ['id', 'user', 'status', 'date_joined', 'is_active']


class EventSerializer(serializers.ModelSerializer):

    invitations = InvitationSerializer(many=True)

    class Meta:
        model = Event
        fields = ['id', 'name', 'admin_id', 'event_settings', 'location_name',
                  'location_lat', 'location_lng', 'number_of_attendees', 'event_datetime', 'invitations']


class CreateEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['id', 'name', 'admin_id', 'event_settings', 'location_name',
                  'location_lat', 'location_lng', 'number_of_attendees', 'event_datetime']


# this is a read only path to get information about the event without logging in, to accept an invite, you need to log in
class PublicInvitationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invitation
        fields = ['id', 'user', 'event', 'status', 'date_joined', 'is_active']


class InvitationWithEventsSerializer(serializers.ModelSerializer):

    event = CreateEventSerializer()

    class Meta:
        model = Invitation
        fields = ['id', 'user', 'event', 'status',
                  'date_joined', 'is_active']
