from .models import Like,Comment,Link,Download
from core.serializer import ProfileSerializer,serializers,PageSerializer


class LikeSerializer(serializers.ModelSerializer):
    profile=ProfileSerializer()
    class Meta:
        model=Like
        fields=['id', 'profile']
 
 

class CommentSerializer(serializers.ModelSerializer):
    profile=ProfileSerializer()
    page=PageSerializer()
    class Meta:
        model=Comment
        fields=['id','page', 'profile','comment','persian_datetime_added']
 

class LinkSerializer(serializers.ModelSerializer):
    page=PageSerializer()
    # profile=ProfileSerializer()
    class Meta:
        model=Link
        fields=['id','page', 'url','priority','title','get_edit_url','get_delete_url']
 

class DownloadSerializer(serializers.ModelSerializer):
    page=PageSerializer()
    profile=ProfileSerializer()
    class Meta:
        model=Download
        fields=['id','page','get_download_url', 'profile','title','get_edit_url','get_delete_url']
 
