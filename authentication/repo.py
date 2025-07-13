from .models import Profile,Person,FAILED,SUCCEED,APP_NAME


 
class PersonRepo():
    def __init__(self,request,*args, **kwargs):
        self.request=request
        self.me=None
        # profile=ProfileRepo(request=request).me
        self.objects=Person.objects

        
       

        # if profile is not None:
        #     self.me=self.objects.filter(profile=profile).first()
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

        # if 'profile_id' in kwargs:
        #     if Person.objects.filter(profile_id=kwargs['profile_id']).first() is not None:
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
            
        if 'profile_id' in kwargs and kwargs['profile_id']>0:
            person.profile_id=kwargs["profile_id"]
            
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
        if 'person_category_id' in kwargs and kwargs["person_category_id"] is not None:
            person_category_id=kwargs["person_category_id"]
            person_category=PersonCategory.objects.filter(pk=person_category_id).first()
            if person_category is not None:
                categories=[person_category.code]
         
            
        if 'person_account_categories' in kwargs:
            person_account_categories=kwargs["person_account_categories"]
             
 
        (result,message,person)=person.save()
        if result==FAILED:
            return result,message,person
        


        for person_account_category in person_account_categories: 
            person_category=PersonCategory.objects.filter(pk=person_account_category).first()
            person_account=PersonAccount(person=person,person_category=person_category)
            person_account.person=person
            person_account.person_category=person_category 
            person_account.save()
            pass
 
        return result,message,person




class ProfileRepo():
    def __init__(self,request,*args, **kwargs):
        self.request=request 
        self.me=None
        self.objects=Profile.objects
        if self.request.user.is_authenticated:
            self.me=Profile.objects.filter(user=request.user).first()
    def logout(self,*args, **kwargs):
        pass        
    def login(self,*args, **kwargs):
        pass        
    def profile(self,*args, **kwargs):
        if "profile_id" in kwargs and kwargs["profile_id"] is not None:
            return self.objects.filter(pk=kwargs['profile_id']).first()
        if "pk" in kwargs and kwargs["pk"] is not None:
            return self.objects.filter(pk=kwargs['pk']).first() 
        if "id" in kwargs and kwargs["id"] is not None:
            return self.objects.filter(pk=kwargs['id']).first() 
        if "code" in kwargs and kwargs["code"] is not None:
            return self.objects.filter(code=kwargs['code']).first()