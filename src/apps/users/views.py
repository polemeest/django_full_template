from django.shortcuts import render
from rest_framework.generics import ListAPIView
from rest_framework import permissions

from .serializers import UserSerializer
from .models import User


class UserListView(ListAPIView):
    """Получить всех пользователей"""
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [permissions.IsAuthenticated]