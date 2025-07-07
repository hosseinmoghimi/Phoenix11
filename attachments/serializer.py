from .models import Like,Comment,Link,Download
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
 

class LinkSerializer(serializers.ModelSerializer):
    # profile=ProfileSerializer()
    class Meta:
        model=Link
        fields=['id', 'url','priority','title','get_edit_url','get_delete_url']
 

class DownloadSerializer(serializers.ModelSerializer):
    profile=ProfileSerializer()
    class Meta:
        model=Download
        fields=['id','get_download_url', 'profile','title','get_edit_url','get_delete_url']
 
