from gc import get_objects
from http import server
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from events.models import Event, Invitation
from events.serializers import EventSerializer, PublicInvitationSerializer, CreateEventSerializer, InvitationWithEventsSerializer
from rest_framework.views import APIView
from django.http import Http404
from rest_framework.permissions import AllowAny
import json


@api_view(['GET', 'POST'])
def event_list(request, format=None):

    if request.method == "GET":

        events = request.user.event_set.all()

        serializer = EventSerializer(events, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = CreateEventSerializer(data=request.data)
        if serializer.is_valid():
            newEvent = serializer.save()
            invitation = Invitation(
                user=request.user, event=newEvent, status="accepted", is_active=True)
            invitation.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def event_detail(request, pk, format=None):
    """
    Retrieve, update or delete a code event.
    """
    try:
        event = Event.objects.get(pk=pk)
    except Event.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':

        serializer = EventSerializer(event)
        return Response(serializer.data)

    elif request.method == 'PUT':
        # if user is admin
        serializer = EventSerializer(event, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        # if user is admin
        event.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class PublicEventDetail(APIView):
    authentication_classes = []

    permission_classes = [AllowAny]

    def get_object(self, pk):
        try:
            return Event.objects.filter(invitations=pk)[0]

        except Invitation.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        serializer = EventSerializer(self.get_object(pk))
        return Response(serializer.data)


class InvitationList(APIView):

    def get(self, request, format=None):

        invitations = Invitation.objects.filter(user=request.user)
        serializer = InvitationWithEventsSerializer(invitations, many=True)

        return Response(serializer.data)

    def post(self, request, format=None):
        # should really just use the user from authentication, to do

        serializer = PublicInvitationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
