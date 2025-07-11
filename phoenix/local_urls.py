from django.contrib import admin
from django.urls import path,include,re_path
from django.views.static import serve
from phoenix.server_settings import QRCODE_ROOT,STATIC_ROOT,MEDIA_ROOT
urlpatterns = [ 
    path('', include('core.urls')),
    path('core/', include('core.urls')),
    path('admin/', admin.site.urls),
    path('log/', include('log.urls')),
    path('authentication/', include('authentication.urls')),
    path('accounting/', include('accounting.urls')),
    path('market/', include('market.urls')),
    path('chef/', include('chef.urls')),
    path('utility/', include('utility.urls')),
    path('organization/', include('organization.urls')),
    path('pm/', include('projectmanager.urls')),
    path('school/', include('school.urls')),
    path('attachments/', include('attachments.urls')),
    path('warehouse/', include('warehouse.urls')),
    
    
    
    re_path(r'^qrcode/(?P<path>.*)$', serve, {'document_root': QRCODE_ROOT}),
    re_path(r'^static/(?P<path>.*)$', serve, {'document_root': STATIC_ROOT}),
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': MEDIA_ROOT}),


]
