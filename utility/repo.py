from .models import Parameter,Picture,ClipBoardItem,MyLink
from utility.constants import *
from django.db.models import Q
from authentication.repo import PersonRepo
# from authentication.repo import PersonRepo
from .apps import APP_NAME

from .log import leolog


class ClipBoardItemRepo:
    
    def __init__(self,*args, **kwargs):
        self.app_name=""
        self.request=None
        self.user=None
        if 'app_name' in kwargs:
            self.app_name=kwargs['app_name']
        else:
            self.app_name=None
        if 'request' in kwargs:
            self.request=kwargs['request']
            self.user=self.request.user 
        self.me_person=PersonRepo(request=self.request).me
        self.objects=ClipBoardItem.objects.filter(person=self.me_person)


    def list(self,*args, **kwargs):
        return self.objects.all()
     
    def add_clipboard_item(self,*args,**kwargs):
        result=FAILED
        if self.me_person is None:
            return FAILED
        clip_board_item=ClipBoardItem(person_id=self.me_person.id,*args,**kwargs)
        clip_board_item.save()

        clip_board_item_list=ClipBoardItem.objects.filter(person_id=self.me_person)
        if len(clip_board_item_list)>CLIPBODRD_MAX_LENGTH :
            clip_board_item_list.first().delete()
        result=SUCCEED
        return result




class MyLinkRepo:
    
    def __init__(self,*args, **kwargs):
        self.app_name=""
        self.request=None
        self.user=None
        if 'app_name' in kwargs:
            self.app_name=kwargs['app_name']
        else:
            self.app_name=None
        if 'request' in kwargs:
            self.request=kwargs['request']
            self.user=self.request.user 
        self.me_person=PersonRepo(request=self.request).me
        self.objects=MyLink.objects.filter(person=self.me_person).order_by('priority')


    def list(self,*args, **kwargs):
        return self.objects.all()
    def delete_my_link(self,my_link_id):
        result,my_links=FAILED,[]
        my_link=MyLink.objects.filter(person_id=self.me_person.id).filter(id=my_link_id).first()
        if my_link is not None:
            my_link.delete()
            result=SUCCEED
            my_links= MyLink.objects.filter(person_id=self.me_person.id).order_by('link__priority')
        return result,my_links
    def add_my_link(self,*args,**kwargs):
        result=FAILED
        if self.me_person is None:
            return FAILED
        from attachments.models import Link
        my_link=MyLink(person_id=self.me_person.id)
        if 'title' in kwargs:
            my_link.title=kwargs['title']
        if 'url' in kwargs:
            my_link.url=kwargs['url']
        if 'priority' in kwargs:
            my_link.priority=kwargs['priority']
        my_link.person_id=self.me_person.id
        my_link.save()

        my_link_list=MyLink.objects.filter(person_id=self.me_person).order_by('link__priority')
        if len(my_link_list)>MY_LINKS_LENGTH :
            my_link_list.first().delete()
        result=SUCCEED
        return result


class PictureRepo:
    
    def __init__(self,*args, **kwargs):
        self.app_name=""
        self.request=None
        self.user=None
        if 'app_name' in kwargs:
            self.app_name=kwargs['app_name']
        else:
            self.app_name=None
        if 'request' in kwargs:
            self.request=kwargs['request']
            self.user=self.request.user 
        self.person=PersonRepo(request=self.request).me
        self.objects=Picture.objects.filter(app_name=self.app_name)
    def list(self,*args, **kwargs):
        return self.objects.filter(app_name=self.app_name)
    def picture(self,*args, **kwargs):
        if 'app_name' in kwargs:
            app_name=kwargs['app_name']
            self.app_name=app_name
            self.objects=Picture.objects.filter(app_name=app_name)

        pk=0
        name=""
        picture=None
        if 'name' in kwargs:
            name=kwargs['name']
            if name=="":
                return
            picture= self.objects.filter(app_name=self.app_name).filter(name=name).first()
            if picture is None:
                picture=Picture(app_name=self.app_name,name=name)
                picture.app_name=self.app_name
                picture.name=name
                if 'default' in kwargs:
                    picture.image_origin=kwargs['default']
                picture.save()
                return picture
            # (picture,res) = self.objects.get_or_create(name=name,app_name=self.app_name)
            # picture = self.objects.filter(name=name).filter(app_name=self.app_name).first()
            return picture
        if 'pk' in kwargs:
            pk=kwargs['pk']
        if 'picture_id' in kwargs:
            pk=kwargs['picture_id']
        if pk>0:
            picture= self.objects.filter(pk=pk).first()
        return picture

    def get(self,*args, **kwargs):
        return self.picture(*args, **kwargs)

class ParameterRepo:    
    def __init__(self,request,*args, **kwargs):
        self.request=None 
        self.app_name=None
        self.person=None
        self.request=request
        if request is not None:
            self.user=self.request.user 
        self.objects=Parameter.objects
        if 'app_name' in kwargs :
            self.app_name=kwargs['app_name']
            self.objects=Parameter.objects.filter(app_name=self.app_name)
        else:
            self.app_name=None
        # self.person=PersonRepo(request=self.request).me
        
        if 'force' in kwargs and kwargs['force']:
            self.objects=Parameter.objects.all()
    
    def change_parameter_temp_deleted(self,*args, **kwargs):
        if not self.request.user.has_perm(APP_NAME+'.change_parameter'):
            return None
        parameter_id=kwargs['parameter_id'] if 'parameter_id' in kwargs else None
        parameter_name=kwargs['parameter_name'] if 'parameter_name' in kwargs else None
        parameter_value=kwargs['parameter_value'] if 'parameter_value' in kwargs else None
        app_name=self.app_name
        if parameter_id is not None:
            parameter=Parameter.objects.filter(pk=parameter_id).first()
            if parameter is None:
                return None
        elif parameter_name is not None and app_name is not None:
            parameter=Parameter.objects.filter(app_name=app_name).filter(name=parameter_name).first()
            if parameter is None:
                parameter=Parameter(app_name=app_name,name=parameter_name,value_origin="")
                parameter.save()
        
        parameter.origin_value=parameter_value
        parameter.save()
        return parameter

    
    def set(self,*args, **kwargs):
         
        return self.set_parameter(*args, **kwargs)
    
    def set_parameter(self,*args, **kwargs):
         
        value=kwargs['value']
        name=kwargs['name']
        app_name=kwargs['app_name']
        if not self.request.user.has_perm(APP_NAME+'.change_parameter'):
            message='مجوز دسترسی شما برای این کار کافی نمی باشد. '
            return FAILED,message,None
        Parameter.objects.filter(app_name=app_name).filter(name=name).delete()
        if value is None:
            value=name
        parameter=self.parameter()
        parameter.name=name
        parameter.app_name=app_name
        parameter.origin_value=value
        parameter.save()
        message="پارامتر با موفقیت تغییر یافت."
        return SUCCEED,message,parameter
     
    
    
    def parameter(self,*args, **kwargs):
        
        if 'app_name' in kwargs:
            self.app_name=kwargs['app_name']
            self.objects=Parameter.objects.filter(app_name=self.app_name)

        parameter=None
        parameter_name=""
        if 'parameter_name' in kwargs:
            parameter_name=kwargs['parameter_name']
        if 'name' in kwargs:
            parameter_name=kwargs['name']
        parameter= self.objects.filter(name=parameter_name).first()
        if parameter is None:
            default=parameter_name
            if 'default' in kwargs:
                default=kwargs['default']
            
            parameter=Parameter(name=parameter_name,app_name=self.app_name,origin_value=default)
            parameter.save()

        if 'id' in kwargs:
            parameter= self.objects.filter(name=kwargs['id']).first()
        if 'parameter_id' in kwargs:
            parameter= self.objects.filter(name=kwargs['parameter_id']).first()
        if 'pk' in kwargs:
            parameter= self.objects.filter(name=kwargs['pk']).first()
            
        return parameter

        

    def list(self,*args, **kwargs):
        objects= self.objects
        
        if 'app_name' in kwargs:
            self.app_name=kwargs['app_name']
            objects=objects.filter(app_name=self.app_name)
        return objects.all()

