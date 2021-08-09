from rest_framework import serializers

from .models import User


class UserCreateSerializer(serializers.ModelSerializer):
    extra_kwargs = {'password': {'write_only': True}}

    class Meta:
        model = User
        fields = ('email', 'username', 'password')

    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username',)
