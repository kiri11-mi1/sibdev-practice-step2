from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from . import serializers
from .models import User


class UserView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer


class AboutUserView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.AboutUserSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        queryset = request.user
        serializer = self.get_serializer(queryset)
        return Response(serializer.data)
