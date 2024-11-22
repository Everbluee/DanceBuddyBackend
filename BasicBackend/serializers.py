from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import *

class DanceClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = DanceClass
        fields = '__all__'

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = '__all__'