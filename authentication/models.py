from django.db import models
from django.utils.translation import gettext as _
from .enums import *
from django.conf import settings
from utility.models import LinkHelper
from phoenix.settings import MEDIA_URL,STATIC_URL
from .apps import APP_NAME
from utility.models import ImageHelper
from utility.constants import FAILED,SUCCEED
IMAGE_FOLDER=APP_NAME+"/images/"
from utility.enums import *

class Profile(models.Model,LinkHelper):

    full_name=models.CharField(_("full_name"), max_length=50)
    user=models.OneToOneField(settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,null=True,blank=True)
    image_origin=models.ImageField(_("تصویر"),null=True,blank=True, upload_to=IMAGE_FOLDER+"profile/", height_field=None, width_field=None, max_length=None)
    enabled=models.BooleanField(_("فعال"),default=True)
    class_name="profile"
    app_name=APP_NAME
    class Meta:
        verbose_name = _("Profile")
        verbose_name_plural = _("Profiles")

    def __str__(self):
        return self.full_name
  
    @property
    def image(self):
        if self.image_origin is None or not self.image_origin:
            return f'{STATIC_URL}{APP_NAME}/img/default-avatar.png'
        return f"{MEDIA_URL}{self.image_origin}"
    

class Person(models.Model,ImageHelper,LinkHelper):
    profile=models.ForeignKey("profile",null=True,blank=True, verbose_name=_("profile"), on_delete=models.CASCADE)
    prefix=models.CharField(_("پیشوند"),default=PersonPrefixEnum.MR,choices=PersonPrefixEnum.choices, max_length=50)
    first_name=models.CharField(_("نام"), max_length=50)
    last_name=models.CharField(_("نام خانوادگی"), max_length=50)
    mobile=models.CharField(_("شماره همراه"),null=True,blank=True, max_length=50)
    email=models.CharField(_("email"),null=True,blank=True, max_length=50)
    bio=models.CharField(_("بیو"),null=True,blank=True, max_length=50)
    address=models.CharField(_("آدرس"),null=True,blank=True, max_length=50)
    full_name=models.CharField(_("full_name"),null=True,blank=True, max_length=150)
    image_origin=models.ImageField(_("تصویر"),null=True,blank=True, upload_to=IMAGE_FOLDER+"profile/", height_field=None, width_field=None, max_length=None)
    gender=models.CharField(_("جنسیت"),choices=GenderEnum.choices,default=GenderEnum.MALE, max_length=50)
    type=models.CharField(_("ماهیت"),choices=PersonTypeEnum.choices,default=PersonTypeEnum.FREE, max_length=50)
    type2=models.CharField(_("نوع"),choices=PersonType2Enum.choices,default=PersonType2Enum.HAGHIGHI, max_length=50)
    melli_code=models.CharField(_("کد ملی"),null=True,blank=True, max_length=10)
    class_name='person'
    app_name=APP_NAME

    class Meta:
        verbose_name = _("Person")
        verbose_name_plural = _("اشخاص")

   
    @property
    def full_name_(self):
        full_name=""
        if self.prefix:
            full_name=self.prefix
            
        if len(full_name)>0:
            full_name+=" "
           
        if self.first_name:
            full_name+=self.first_name 

            
            
        if len(full_name)>0:
            full_name+=" "
           
        if self.last_name:
            full_name+=self.last_name 

        return full_name



    def __str__(self):
        return self.full_name

   

    def save(self,*args, **kwargs):
        result,message,person=FAILED,"",None
        # others=Person.objects.exclude(pk=self.pk)
        # if others.filter(code=self.code).first() is not None:
        #     message="کد تکراری می باشد."
        #     return result,message,person
        # self.
        # 
        self.full_name=self.full_name_
        super(Person,self).save()
        result=SUCCEED
        message=" با موفقیت اضافه گردید."
        person=self
        return result,message,person    

