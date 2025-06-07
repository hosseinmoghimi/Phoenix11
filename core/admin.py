from django.contrib import admin

from .models import Page,EventCategory,Event,Comment,Like
admin.site.register(Page)
admin.site.register(EventCategory)
admin.site.register(Event)
admin.site.register(Comment)
admin.site.register(Like)