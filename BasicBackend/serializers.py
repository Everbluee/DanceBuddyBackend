from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = '__all__'

    def get_profile_picture(self, obj):
        return obj.image.url


class UserInClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['id', 'first_name', 'last_name']


class DanceClassSerializer(serializers.ModelSerializer):
    users = UserInClassSerializer(many=True, read_only=True)

    class Meta:
        model = DanceClass
        fields = ['id', 'title', 'level', 'description', 'time', 'days', 'instructor', 'users']


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'

    def get_event_picture(self, obj):
        return obj.image.url
