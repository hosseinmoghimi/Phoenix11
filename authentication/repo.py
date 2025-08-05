from .models import Person,FAILED,SUCCEED,APP_NAME
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from utility.log import leolog

 
class PersonRepo():
    def user(self,*args, **kwargs):
        user_id=0
        if 'user_id' in kwargs:
            user_id=kwargs['user_id']
            return User.objects.filter(pk=user_id).first()
        return User.objects.filter(pk=0).first()
    def __init__(self,request,*args, **kwargs):
        self.me=None
        self.request=request
        if request.user.is_authenticated:
            if self.request.user.has_perm(APP_NAME+'.view_person'):
                self.objects=Person.objects.all()
            else:
                self.objects=Person.objects.filter(user_id=request.user.id) 
        self.me=Person.objects.filter(user_id=request.user.id).first()
        # person=PersonRepo(request=request).me

        
       

        # if person is not None:
        #     self.me=self.objects.filter(person=person).first()
    def list(self,*args, **kwargs):
        objects=self.objects
        from django.db.models import Q
        if "search_for" in kwargs:
            search_for=kwargs["search_for"]
            objects=objects.filter(Q(first_name__contains=search_for) |Q(last_name__contains=search_for) | Q(melli_code__contains=search_for) )
        return objects.all()
    def change_image(self,person_id,image):
        person=self.person(person_id=person_id)
        if person is not None:
            person.image_origin = image
            person.save()
            return SUCCEED
        return FAILED
    
    def person(self,*args, **kwargs):
        if "person_id" in kwargs and kwargs["person_id"] is not None:
            return self.objects.filter(pk=kwargs['person_id']).first()
        if "person" in kwargs:
            return kwargs['person'] 
        if "pk" in kwargs and kwargs["pk"] is not None:
            return self.objects.filter(pk=kwargs['pk']).first() 
        if "id" in kwargs and kwargs["id"] is not None:
            return self.objects.filter(pk=kwargs['id']).first() 
        if "code" in kwargs and kwargs["code"] is not None:
            return self.objects.filter(code=kwargs['code']).first()
             
        if "account_code" in kwargs and kwargs["account_code"] is not None:
            a= self.objects.filter(code=kwargs['account_code']).first() 
            if a is not None:
                return a
            else:
                try:
                    a= self.objects.filter(pure_code=filter_number(kwargs['account_code'])).first() 
                    if a is not None:
                        return a
                except:
                    pass
       
    def delete_all(self,*args,**kwargs):
        result,message=FAILED,''
        if not self.request.user.has_perm(APP_NAME+".delete_person"):
            message="دسترسی غیر مجاز"
            return result,message
        # PersonCategory.objects.all().delete()
        Person.objects.all().delete()
        result=SUCCEED
        message="همه اشخاص حذف شدند."
        return result,message
    
    def add_person(self,*args,**kwargs):
        result,message,person=FAILED,"",None
        if not self.request.user.has_perm(APP_NAME+".add_person"):
            message="دسترسی غیر مجاز"
            return result,message,person

        person=Person()
        person_category_id=0
        categories=[]
        person_account_categories=[]

        # if 'person_id' in kwargs:
        #     if Person.objects.filter(person_id=kwargs['person_id']).first() is not None:
        #         message="کد پروفایل وارد شده تکراری است."
        #         person=None
        #         return result,message,person
        if 'melli_code' in kwargs:
            melli_code=kwargs['melli_code']

            if melli_code is not None and len(melli_code)>0 and Person.objects.filter(melli_code=melli_code).first() is not None:
                message="کد ملی وارد شده تکراری است."
                person=None
                return result,message,person

  
        if 'type2' in kwargs:
            person.type2=kwargs["type2"]
        if 'type' in kwargs:
            person.type=kwargs["type"]
        if 'melli_code' in kwargs:
            person.melli_code=kwargs["melli_code"]
        if 'title' in kwargs:
            person.title=kwargs["title"]
            
        if 'person_id' in kwargs and kwargs['person_id']>0:
            person=PersonRepo(request=self.request).person(person_id=kwargs['person_id'])
            person.person=person
        if 'color' in kwargs:
            person.color=kwargs["color"]
        if 'first_name' in kwargs:
            person.first_name=kwargs["first_name"]
        if 'last_name' in kwargs:
            person.last_name=kwargs["last_name"]
        if 'bio' in kwargs:
            person.bio=kwargs["bio"]
        if 'email' in kwargs:
            person.email=kwargs["email"]
        if 'mobile' in kwargs:
            person.mobile=kwargs["mobile"]
        if 'prefix' in kwargs:
            person.prefix=kwargs["prefix"]
        if 'gender' in kwargs:
            person.gender=kwargs["gender"]
        if 'address' in kwargs:
            person.address=kwargs["address"]  
        if 'type' in kwargs:
            person.type=kwargs["type"] 
         
          
        (result,message,person)=person.save()
        if result==FAILED:
            return result,message,person
        

 
        return result,message,person


    def logout(self,*args, **kwargs):
        if 'request' in kwargs:
            logout(request=kwargs['request'])
        else:
            logout(request=self.request)
    def login(self,*args, **kwargs):
        request=self.request
        from log.repo import LogRepo
        logout(request=request)
        if 'user' in kwargs:
            user=kwargs['user']
            if user is not None:
                login(request,user)
                if user.is_authenticated:
                    return (request,user)
        if 'username' in kwargs and 'password' in kwargs:
            user=authenticate(request=request,username=kwargs['username'],password=kwargs['password'])
            if user is not None:
                login(request,user)
                if user.is_authenticated:
                    person=Person.objects.filter(user=user).first()
                    description='لاگین با موفقیت انجام شد.'
                    title='لاگین'
                    LogRepo(request=self.request).add_log(title=title,person=person,app_name=APP_NAME,description=description)
                    return (request,user)
        LogRepo(request=self.request).add_log(title="try to login",app_name=APP_NAME,description="try to login username:"+kwargs['username']+" , password : "+kwargs['password'])
    
 