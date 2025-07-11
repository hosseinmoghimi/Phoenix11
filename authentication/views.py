from django.shortcuts import render,redirect,reverse
from phoenix.server_settings import DEBUG,ADMIN_URL,MEDIA_URL,SITE_URL,STATIC_URL
from .repo import ProfileRepo
from django.views import View
from .serializer import PersonSerializer
from .repo import PersonRepo,FAILED,SUCCEED
from .forms import *
from .apps import APP_NAME
from phoenix.server_apps import phoenix_apps
from utility.calendar import PersianCalendar
from core.views import CoreContext,ParameterRepo,PictureRepo
import json

LAYOUT_PARENT='phoenix/layout.html'
TEMPLATE_ROOT='authentication/'
WIDE_LAYOUT="WIDE_LAYOUT"
NO_FOOTER="NO_FOOTER"
NO_NAVBAR="NO_NAVBAR"

def getContext(request,*args, **kwargs):
    context=CoreContext(app_name=APP_NAME,request=request)
 
    context['LAYOUT_PARENT']=LAYOUT_PARENT
    return context
 
def AddPersonContext(request,*args, **kwargs):
    context={}
    from .enums import PersonType2Enum,PersonTypeEnum
    from utility.enums import PersonPrefixEnum,GenderEnum
    context['prefixes']=(i[0] for i in PersonPrefixEnum.choices)
    context['genders']=(i[0] for i in GenderEnum.choices)
    context['types']=(i[0] for i in PersonTypeEnum.choices)
    context['types2']=(i[0] for i in PersonType2Enum.choices)

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
class ChangePersonImageView(View):
    def post(self,request,*args, **kwargs):
        profile_id=0
        if 'pk' in kwargs:
            profile_id=kwargs['pk']
        log=1
        if request.method=='POST':
            log=2
            change_person_image_form=ChangePersonImageForm(request.POST,request.FILES)
            if change_person_image_form.is_valid():
                log=3              
                person_id=change_person_image_form.cleaned_data['person_id']
                image=request.FILES['image']
                result=PersonRepo(request=request).change_image(person_id=person_id,
                image=image,
                )
        return redirect(reverse(APP_NAME+":person",kwargs={'pk':person_id}))

class PersonsView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        context['name3']="name 3333"
        persons=PersonRepo(request=request).list(*args, **kwargs)
        persons_s=json.dumps(PersonSerializer(persons,many=True).data)
        context['persons']=persons
        context['persons_s']=persons_s
        if request.user.has_perm(APP_NAME+'.add_person'):
            context['add_person_form']=AddPersonForm()
            context.update(AddPersonContext(request=request))
        return render(request,TEMPLATE_ROOT+"persons.html",context)
class PersonView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        person=PersonRepo(request=request).person(*args, **kwargs)
        context['person']=person
        person_s=json.dumps(PersonSerializer(person).data)
        context['person_s']=person_s
        if request.user.has_perm(APP_NAME+'.change_person'):
            context['change_person_image_form']=ChangePersonImageForm()
        return render(request,TEMPLATE_ROOT+"person.html",context)
# Create your views here.

class LoginView(View):
    def get(self,request,*args, **kwargs): 
        messages=[]
        if 'messages' in kwargs:
            messages=kwargs['messages']
        context=getContext(request=request)
        context['login_form_header_image']=PictureRepo(request=request,app_name=APP_NAME).picture(name="تصویر لاگین")
        context['messages']=messages
        if 'next' in request.GET:
            context['next']=request.GET['next']
        else:
            context['next']=SITE_URL

        ProfileRepo(request=request).logout(request)
        context['login_form']=LoginForm()
        context['build_absolute_uri']=request.build_absolute_uri()
        build_absolute_uri=request.build_absolute_uri()
        ONLY_HTTPS=ParameterRepo(request=request,app_name=APP_NAME).parameter(name="فقط HTTPS",default=False).boolean_value
        if ONLY_HTTPS and "http://" in build_absolute_uri :
            build_absolute_uri=build_absolute_uri.replace("http:","https:")
            return redirect(build_absolute_uri)
        return render(request,TEMPLATE_ROOT+"login.html",context)
    def post(self,request,*args, **kwargs):
        context=getContext(request=request) 
        return render(request,TEMPLATE_ROOT+"login.html",context)
# Create your views here.

class ChangePasswordView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request) 
           
        return render(request,TEMPLATE_ROOT+"login.html",context)
# Create your views here.
