from django.db import models
from django.utils.translation import gettext as _
from django.conf import settings
from utility.models import LinkHelper
from phoenix.settings import MEDIA_URL,STATIC_URL
from .apps import APP_NAME
IMAGE_FOLDER=APP_NAME+"/images/"


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