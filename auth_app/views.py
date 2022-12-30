from django.shortcuts import render
from rest_framework.generics import CreateAPIView
from .serializers import LoginSerializer
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.serializers import ValidationError
# Create your views here.
class LoginView(CreateAPIView):
    serializer_class = LoginSerializer

    def perform_create(self, serializer):
        email = serializer.validated_data.get('email')
        password = serializer.validated_data.get('password')
        user = authenticate(username=email,password=password)
        if user:
            token, created = Token.objects.get_or_create(user=user)
            print(token)
            serializer.validated_data['token'] = token.key
        else:
            raise ValidationError('usernamme or password or both are wrong')
