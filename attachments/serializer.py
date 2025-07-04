from rest_framework import serializers
from .models import Like
from core.serializer import ProfileSerializer


class LikeSerializer(serializers.ModelSerializer):
    profile=ProfileSerializer()
    class Meta:
        model=Like
        fields=['id', 'profile']
 
