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
from phoenix.server_settings import UPLOAD_ROOT,QRCODE_ROOT,QRCODE_URL,STATIC_URL,MEDIA_URL,ADMIN_URL,FULL_SITE_URL
IMAGE_FOLDER = "images/"
upload_storage = FileSystemStorage(location=UPLOAD_ROOT, base_url='/uploads')


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
    

    def save(self):
        if self.class_name is None or self.class_name=="":
            self.class_name="page"
        if self.app_name is None or self.app_name=="":
            self.app_name="core"
        super(Page,self).save()

    # def likes_count(self):
    #     return len(PageLike.objects.filter(page_id=self.id))

     

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

