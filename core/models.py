from django.db import models
from .apps import APP_NAME
from django.utils.translation import gettext as _
from utility.qrcode import generate_qrcode
from utility.enums import *
from .enums import *
from utility.calendar import PersianCalendar
from utility.models import LinkHelper,ImageHelper,DateTimeHelper
from tinymce.models import HTMLField
from django.shortcuts import reverse
from django.core.files.storage import FileSystemStorage
from utility.constants import FAILED,SUCCEED
from phoenix.server_settings import UPLOAD_ROOT,QRCODE_ROOT,QRCODE_URL,STATIC_URL,MEDIA_URL,ADMIN_URL,FULL_SITE_URL
IMAGE_FOLDER = "images/"
PAGE_TITLE_SEPERATOR=' / '
upload_storage = FileSystemStorage(location=UPLOAD_ROOT, base_url='/uploads')
from utility.enums import class_title

class Page(models.Model,LinkHelper,ImageHelper):
    parent=models.ForeignKey("page",null=True,blank=True,related_name="childs", verbose_name=_("parent"), on_delete=models.CASCADE)
    app_name=models.CharField(_("app_name"),blank=True, max_length=50)
    class_name=models.CharField(_("class_name"),blank=True, max_length=50)
    title=models.CharField(_("title"), max_length=50)
    short_description=HTMLField(_("short_description"),null=True,blank=True, max_length=5000)
    description=HTMLField(_("description"),null=True,blank=True, max_length=50000)
    related_pages=models.ManyToManyField("page",blank=True, verbose_name=_("related_pages"))
    date_added = models.DateTimeField(_("date_added"), auto_now=False, auto_now_add=True)
    meta_data=models.CharField(_("meta_data"),default="",null=True,blank=True, max_length=500)
    priority = models.IntegerField(_("ترتیب"), default=1000)
    thumbnail_origin = models.ImageField(_("تصویر کوچک"), upload_to=IMAGE_FOLDER+'ImageBase/Thumbnail/',null=True, blank=True, height_field=None, width_field=None, max_length=None)
    header_origin = models.ImageField(_("تصویر سربرگ"), upload_to=IMAGE_FOLDER+'ImageBase/Header/',null=True, blank=True, height_field=None, width_field=None, max_length=None)
    color=models.CharField(_("color"),choices=ColorEnum.choices,default=ColorEnum.PRIMARY,max_length=50)
    locations=models.ManyToManyField("attachments.location", blank=True,verbose_name=_("locations"))
    
       
    def set_priority(self,request,*args, **kwargs):
        result,message,priority=FAILED,"",100
        if not request.user.has_perm(APP_NAME+".change_page"):
            return result,message,priority
        priority=kwargs['priority']
        page_id=kwargs['page_id']
        page=Page.objects.filter(pk=page_id).first()
        if page is not None:
            page.priority=priority
            page.save()
        result=SUCCEED
        return result,message,priority

    def save(self,*args, **kwargs):
        if self.class_name is None or self.class_name=="":
            self.class_name="page"
        if self.app_name is None or self.app_name=="":
            self.app_name="core"
        super(Page,self).save()

    # def likes_count(self):
    #     return len(PageLike.objects.filter(page_id=self.id))

     

    def get_qrcode_url(self):
        if self.pk is None:
            super(Page,self).save()
        import os
        file_path = QRCODE_ROOT
        file_name=self.class_name+str(self.pk)+".svg"
        file_address=os.path.join(QRCODE_ROOT,file_name)
        if not os.path.exists(file_address):
            content=FULL_SITE_URL[0:-1]+self.get_absolute_url()
            generate_qrcode(content=content,file_name=file_name,file_address=file_address,file_path=file_path,)
        return f"{QRCODE_URL}{file_name}"

    def class_title(self):
        return class_title(app_name=self.app_name,class_name=self.class_name)


    # def my_like(self,profile_id):
    #     my_likes=PageLike.objects.filter(page_id=self.id).filter(profile_id=profile_id)
    #     return len(my_likes)>0

    class Meta:
        verbose_name = _("Page")
        verbose_name_plural = _("Pages")

    def __str__(self):
        return self.title

    def get_qrcode_url(self):
        if self.pk is None:
            super(Page,self).save()
        import os
        file_path = QRCODE_ROOT
        file_name=self.class_name+str(self.pk)+".svg"
        file_address=os.path.join(QRCODE_ROOT,file_name)
        if not os.path.exists(file_address):
            content=FULL_SITE_URL[0:-1]+self.get_absolute_url()
            generate_qrcode(content=content,file_name=file_name,file_address=file_address,file_path=file_path,)
        return f"{QRCODE_URL}{file_name}"
    
    def get_absolute_url(self):
        return reverse(self.app_name+":"+self.class_name,kwargs={'pk':self.pk})

    @property  
    def full_title(self):
        if self.parent is None:
            return self.title
        return self.parent.full_title+PAGE_TITLE_SEPERATOR+self.title
 


class EventCategory(models.Model,LinkHelper):
    class_name="eventcategory"
    app_name=APP_NAME
    title=models.CharField(_("title"), max_length=50)
    color_origin=models.CharField(_("color"),choices=ColorEnum.choices,null=True,blank=True, max_length=50)
    @property
    def color(self):
        if self.color_origin:
            return self.color_origin
        if self.title=="هزینه":
            return "danger"
        return 'primary'
    class Meta:
        verbose_name = 'EventCategory'
        verbose_name_plural = 'دسته بندی رویداد ها' 
    def __str__(self):
        return self.title
 

class Event(Page,DateTimeHelper):
    status=models.CharField(_("وضعیت"),choices=EventStatusEnum.choices,default=EventStatusEnum.DRAFT, max_length=50)
    category=models.ForeignKey("eventcategory",null=True,blank=True, verbose_name=_("دسته بندی"), on_delete=models.SET_NULL)
    event_datetime = models.DateTimeField(
        _("event_datetime"), auto_now=False, auto_now_add=False)
    start_datetime = models.DateTimeField(
        _("start_datetime"),null=True,blank=True, auto_now=False, auto_now_add=False)
    end_datetime = models.DateTimeField(
        _("end_datetime"),null=True,blank=True, auto_now=False, auto_now_add=False)
    # adder=models.ForeignKey("authentication.profile", verbose_name=_("profile"), on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        
        from django.utils import timezone
        now =timezone.now()
        if self.event_datetime is None:
            self.event_datetime=now
        if self.start_datetime is None:
            self.start_datetime=now
        if self.end_datetime is None:
            self.end_datetime=now

        if self.app_name is None:
            self.app_name = APP_NAME
        if self.class_name is None:
            self.class_name = "event"
        return super(Event, self).save(*args, **kwargs)

    class Meta:
        verbose_name = _("Event")
        verbose_name_plural = _("رویداد ها")
 
