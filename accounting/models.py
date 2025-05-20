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


class Account(models.Model,LinkHelper,ImageHelper):
    parent=models.ForeignKey("account",null=True,blank=True,related_name="childs", verbose_name=_("parent"), on_delete=models.SET_NULL)
    title=models.CharField(_("title"), max_length=50)
    short_description=HTMLField(_("short_description"),null=True,blank=True, max_length=5000)
    description=HTMLField(_("description"),null=True,blank=True, max_length=50000)
    date_added = models.DateTimeField(_("date_added"), auto_now=False, auto_now_add=True)
    priority = models.IntegerField(_("ترتیب"), default=1000)
    color=models.CharField(_("color"),choices=ColorEnum.choices,default=ColorEnum.PRIMARY,max_length=50)
    

    def save(self):
        super(Account,self).save()
 

    def class_title(self):
        return class_title(app_name=self.app_name,class_name=self.class_name)
 

    class Meta:
        verbose_name = _("Account")
        verbose_name_plural = _("Accounts")

    def __str__(self):
        return self.title
 
