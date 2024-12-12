from django.shortcuts import render
from accounts.serializers import CustomUserSerializer, LoginSerializer
from accounts.models import CustomUser
from rest_framework.generics import GenericAPIView
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token

# Create your views here.
class RegisterView(GenericAPIView):

    serializer_class = CustomUserSerializer
    permission_classes = [permissions.AllowAny]
    authentication_classes = []

    def post(self, request):
        '''
        post method - creates a new user
        '''
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data

        return Response(user_data, status=status.HTTP_201_CREATED)
    

class LoginView(GenericAPIView):

    serializer_class = LoginSerializer
    permission_classes = [permissions.AllowAny]
    authentication_classes = []

    def post(self, request):
        '''
        post method - logs in a user
        '''
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)