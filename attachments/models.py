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
upload_storage = FileSystemStorage(location=UPLOAD_ROOT, base_url='/uploads')
 
class Comment(models.Model,DateTimeHelper):
    page=models.ForeignKey("core.page", verbose_name=_("page"), on_delete=models.CASCADE)
    profile=models.ForeignKey("authentication.profile", verbose_name=_("profile"), on_delete=models.CASCADE)
    comment=HTMLField(verbose_name="comment")
    datetime_added=models.DateTimeField(_("date_added"), auto_now=False, auto_now_add=True)

    class Meta:
        verbose_name = _("Comment")
        verbose_name_plural = _("Comments")

    def __str__(self):
        return f"{self.profile} : {self.page}"
    

class Like(models.Model,DateTimeHelper):
    page=models.ForeignKey("core.page", verbose_name=_("page"), on_delete=models.CASCADE)
    profile=models.ForeignKey("authentication.profile", verbose_name=_("profile"), on_delete=models.CASCADE)
    datetime_added=models.DateTimeField(_("datetime_added"), auto_now=False, auto_now_add=True)

    class Meta:
        verbose_name = _("Like")
        verbose_name_plural = _("Likes")

    def __str__(self):
        return f" {self.profile.full_name} @ {self.page.title}"

    def my_like(self,*args, **kwargs):
        profile_id=0
        if 'profile_id' in kwargs:
            profile_id=kwargs['profile_id']
        if 'profile' in kwargs:
            profile=kwargs['profile']
            profile_id=profile.id
        if 'profile' in kwargs:
            profile=kwargs['profile']
            profile_id=profile.id
        if 'page' in kwargs:
            page=kwargs['page']
        if 'page_id' in kwargs:
            page_id=kwargs['page_id']
        from core.repo import PageRepo,Page
        page=Page.objects.filter(pk=page_id).first()
        my_likes=Like.objects.filter(page_id=page.id).filter(profile_id=profile_id)
        return len(my_likes)>0