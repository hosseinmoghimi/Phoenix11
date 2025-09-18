from django.contrib import admin
from .models import Parameter,Picture,ClipBoardItem,MyLink
admin.site.register(ClipBoardItem)
admin.site.register(Parameter)
admin.site.register(Picture)
admin.site.register(MyLink)