from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import User
from .serializers import UserSerializer
import json

# Create your views here.

@api_view(["GET"])
def get_users(request):
    if request.method != "GET":
        return Response(status.HTTP_400_BAD_REQUEST)

    users = User.objects.all()

    serializer = UserSerializer(users, many=True)
           
    return Response(serializer.data, status.HTTP_200_OK)
