from .models import Like,Comment,Link,Download,Image, Tag
from core.serializer import ProfileSerializer,serializers,PageSerializer
from .models import Area, Location

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model=Location
        fields=['id','title','longitude','location','latitude','title','get_absolute_url']


         
class AreaSerializer(serializers.ModelSerializer):
    class Meta:
        model=Area
        fields=['id','code','color','area','title','get_absolute_url']


          

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
 

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model=Tag
        fields=['id' , 'title','get_absolute_url']
 
class LinkSerializer(serializers.ModelSerializer):
    page=PageSerializer()
    # profile=ProfileSerializer()
    class Meta:
        model=Link
        fields=['id','page', 'url','priority','title','get_edit_url','get_delete_url']
 

 
class ImageSerializer(serializers.ModelSerializer):
    page=PageSerializer()
    # profile=ProfileSerializer()
    class Meta:
        model=Image
        fields=['id','page','title', 'thumbnail','get_absolute_url','image','persian_date_added','priority','title','get_edit_url','get_delete_url']
 

class DownloadSerializer(serializers.ModelSerializer):
    page=PageSerializer()
    profile=ProfileSerializer()
    class Meta:
        model=Download
        fields=['id','page','get_download_url', 'profile','title','get_edit_url','get_delete_url']
 
