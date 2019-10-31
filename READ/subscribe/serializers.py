from rest_framework import serializers
from .models import Subscribe
from user.models import READ_User
from video.serializers import VideoSerializer

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = READ_User
        fields = '__all__'


class SubscribeSerializer(serializers.ModelSerializer):    
    class Meta:
        model = Subscribe
        fields = '__all__'
