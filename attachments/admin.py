from django.contrib import admin

from .models import Like,Comment,Link,Icon,Download,Image
admin.site.register(Like) 
admin.site.register(Comment) 
admin.site.register(Icon) 
admin.site.register(Link) 
admin.site.register(Download) 
admin.site.register(Image) 