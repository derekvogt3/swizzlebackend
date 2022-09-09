from gc import get_objects
from django.shortcuts import render
from rest_framework.views import APIView
from .models import ChatMessage, Event
from rest_framework import status
from rest_framework.response import Response
from .serializers import ChatMessageSerializer
import pdb


class EventMessagesList(APIView):

    def get_message_objects(self, request, pk):

        try:
            event = Event.objects.get(id=pk)

        except Event.DoesNotExist:
            raise status.HTTP_404_NOT_FOUND

        if request.user in event.users.all():
            return event.chat_messages.all()
# get an internal server TypeError: exceptions must derive from BaseException
        else:
            raise status.HTTP_401_UNAUTHORIZED

    def get(self, request, pk, format=None):

        messages = self.get_message_objects(request, pk)
        serializer = ChatMessageSerializer(messages, many=True)
        return Response(serializer.data)
