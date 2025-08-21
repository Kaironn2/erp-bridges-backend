from django.contrib.auth.models import User
from rest_framework import generics, permissions

from .serializers import UserCreateSerializer


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = UserCreateSerializer
