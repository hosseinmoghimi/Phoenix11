from django.shortcuts import render
from phoenix.server_settings import DEBUG,ADMIN_URL,MEDIA_URL,SITE_URL,STATIC_URL

from django.views import View
from .forms import *
from .apps import APP_NAME
from phoenix.server_apps import phoenix_apps
from utility.calendar import PersianCalendar
from phoenix.server_settings import DB_PREFIX_NAME,PUSHER_IS_ENABLE,DEBUG, MEDIA_ROOT,TEMPORARY_ROOT,DB_FILE_PATH,ADMIN_URL, MEDIA_URL, STATIC_URL, SITE_URL
from phoenix.server_apps import phoenix_apps
from django.utils import timezone
from django.http import HttpResponse

LAYOUT_PARENT='phoenix/layout.html'
TEMPLATE_ROOT='utility/'
WIDE_LAYOUT="WIDE_LAYOUT"
NO_FOOTER="NO_FOOTER"
NO_NAVBAR="NO_NAVBAR"
 
def getContext(request,*args, **kwargs):
    from core.views import CoreContext
    context=CoreContext(app_name=APP_NAME,request=request)
 
    context['LAYOUT_PARENT']=LAYOUT_PARENT
    return context


 
class IndexView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        context['name3']="name 3333"
        phoenix_apps=context["phoenix_apps"]
        phoenix_apps=phoenix_apps
        phoenix_apps = sorted(phoenix_apps, key=lambda d: d['priority'])

        context['phoenix_apps']=phoenix_apps
        return render(request,TEMPLATE_ROOT+"index.html",context)
# Create your views here. 



 
class SettingsView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request) 
        return render(request,TEMPLATE_ROOT+"settings.html",context)
# Create your views here. 


class MessageView(View):
    def __init__(self,*args,**kwargs):
        self.links =[]
        self.message ={}
        self.back_url =""
        if 'links' in kwargs:
            self.links=kwargs['links']
        if 'title' in kwargs:
            self.message['title']=kwargs['title']
        if 'body' in kwargs:
            self.message['body']=kwargs['body']

        if 'message' in kwargs:
            self.message=kwargs['message']

        if 'back_url' in kwargs:
            self.back_url=kwargs['back_url']
            

    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        self.back_url = request.META.get('HTTP_REFERER') 
        if 'title' in kwargs:
            self.message['title']=kwargs['title']
        if 'body' in kwargs:
            self.message['body']=kwargs['body']

        if 'message' in kwargs:
            self.message=kwargs['message']

        if 'back_url' in kwargs:
            self.back_url=kwargs['back_url']
        
        context['message']=self.message     
        context['back_url']=self.back_url     
        context['links']=self.links   
        return render(request,TEMPLATE_ROOT+"message.html",context)
# Create your views here.
    def response(self,request,*args,**kwargs):
        return self.get(request,*args,**kwargs)


class ParametersView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        context['WIDE_LAYOUT']=True
        context['phoenix_apps']=phoenix_apps

        return render(request,TEMPLATE_ROOT+"parameters.html",context) 

 
class BackupDBView(View):
    def get(self, request, *args, **kwargs):
        context = getContext(request=request)
        from authentication.views import ProfileRepo
        from django.http import HttpResponse
        from django.utils import timezone
        me = ProfileRepo(request=request).me
        if not request.user.has_perm("core.change_download"):
            mv=MessageView(request=request)
            mv.title="عدم دسترسی مجاز"
            return mv.response()
        
        file_path = str(DB_FILE_PATH)
        # return JsonResponse({'download:':str(file_path)})
        import os
        filename=DB_PREFIX_NAME+"__"+timezone.now().strftime("%Y%m%d_%H_%M_%S")+".sqlite3"
        if os.path.exists(file_path):
            with open(file_path, 'rb') as fh:
                response = HttpResponse(
                    fh.read(), content_type="application/force-download")
                response['Content-Disposition'] = 'inline; filename=' + filename
                return response

  

from .compress import Compress
import os
 
    
class DownloadMediaView(View):
    def get(self, request, *args, **kwargs):
       
            
        if not request.user.has_perm(APP_NAME+".add_parameter"):
            mv=MessageView(request=request)
            mv.title="عدم دسترسی مجاز"
            return mv.response()

        media_zip_file = Compress(folder=MEDIA_ROOT,output_folder=TEMPORARY_ROOT,output_file_name="media").get_output_archive
        # print(10*" media_zip_file")
        # print(media_zip_file)
        
        if media_zip_file is not None:
            # file_path = str(UPLOAD_ROOT)
            # file_path=os.path.join(file_path,"uploads.zip")
            filename="media_"+timezone.now().strftime("%Y%m%d_%H_%M_%S")+".zip"
            # print(10*" file_path")
            # print(file_path)
            file_path=media_zip_file
            if os.path.exists(file_path):
                with open(file_path, 'rb') as fh:
                    response = HttpResponse(
                        fh.read(), content_type="application/force-download")
                    response['Content-Disposition'] = 'inline; filename=' + filename
                    return response
                        
        mv=MessageView(request=request)
        mv.title="عدم دسترسی مجاز"
        return mv.response()
    
class DownloadPrivatesView(View):
    def get(self, request, *args, **kwargs):
         
        if not request.user.has_perm("core.change_download"):
            mv=MessageView(request=request)
            mv.title="عدم دسترسی مجاز"
            return mv.response()   
        from utility.compress import Compress
        import os
        from phoenix.server_settings import UPLOAD_ROOT,TEMPORARY_ROOT
        uploads_zip_file = Compress(folder=UPLOAD_ROOT,output_folder=TEMPORARY_ROOT,output_file_name="uploads").get_output_archive
        
        # print(10*" media_zip_file")
        # print(media_zip_file)
        
        if uploads_zip_file is not None:
            # file_path = str(UPLOAD_ROOT)
            # file_path=os.path.join(file_path,"uploads.zip")
            filename="uploads_"+timezone.now().strftime("%Y%m%d_%H_%M_%S")+".zip"
            # print(10*" file_path")
            # print(file_path)
            file_path=uploads_zip_file
            if os.path.exists(file_path):
                with open(file_path, 'rb') as fh:
                    response = HttpResponse(
                        fh.read(), content_type="application/force-download")
                    response['Content-Disposition'] = 'inline; filename=' + filename
                    return response
                
        mv=MessageView(request=request)
        mv.title="عدم دسترسی مجاز"
        return mv.response()
   