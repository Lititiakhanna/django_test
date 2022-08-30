from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserProf, Login, LoginOperational, LoginClient


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')


class RegisterSerializer(serializers.ModelSerializer):
    user_type = serializers.CharField(max_length=20, default='Client')

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'user_type']

    def create(self, validated_data):
        user = User.objects.create_user(validated_data['username'], validated_data['email'])
        return user


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProf
        fields = ['username', 'password', 'user_type']


class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = Login
        fields = ['username', 'password']


class LoginOperationalSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoginOperational
        fields = ['username', 'fileop']


class LoginClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoginClient
        fields = ['username', 'username_file_uploader']
