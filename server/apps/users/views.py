from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated

from . import serializers
from .models import User


class UserCreateView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.UserCreateSerializer


class UserInfoView(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.UserInfoSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user
