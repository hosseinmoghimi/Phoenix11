from .models import Like,Comment
from core.serializer import ProfileSerializer,serializers


class LikeSerializer(serializers.ModelSerializer):
    profile=ProfileSerializer()
    class Meta:
        model=Like
        fields=['id', 'profile']
 

class CommentSerializer(serializers.ModelSerializer):
    profile=ProfileSerializer()
    class Meta:
        model=Comment
        fields=['id', 'profile','comment','persian_datetime_added']
 
