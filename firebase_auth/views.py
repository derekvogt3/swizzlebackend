from django.shortcuts import render
from .serializers import MyUserSerializer
from rest_framework.response import Response
from rest_framework.views import APIView

# Create your views here.


class CurrentUserView(APIView):
    def get(self, request):
        serializer = MyUserSerializer(request.user)
        return Response(serializer.data)
