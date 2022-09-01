from django.shortcuts import render
from .serializers import MyUserSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import MyUser
from rest_framework import status
# Create your views here.


class CurrentUserView(APIView):
    def get(self, request):
        serializer = MyUserSerializer(request.user)
        return Response(serializer.data)

    def patch(self, request):

        currentUser = MyUser.objects.get(id=request.user.id)

        serializer = MyUserSerializer(currentUser, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
