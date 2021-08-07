from django.contrib.auth import password_validation
from rest_framework import serializers, fields

from .models import User


class UserSerializer(serializers.ModelSerializer):
    password = fields.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('email', 'username', 'password')

    def validate_password(self, value):
        password_validation.validate_password(value, self.instance)
        return value

    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user


class AboutUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username',)
