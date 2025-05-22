from django.db import models
from django.utils.translation import gettext as _
from django.conf import settings



class Profile(models.Model):
    full_name=models.CharField(_("full_name"), max_length=50)
    user=models.OneToOneField(settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,null=True,blank=True)
    class Meta:
        verbose_name = _("Profile")
        verbose_name_plural = _("Profiles")

    def __str__(self):
        return self.full_name
 