from django.db import models
from django.utils.translation import gettext as _

class Profile(models.Model):
    full_name=models.CharField(_("full_name"), max_length=50)

    class Meta:
        verbose_name = _("Profile")
        verbose_name_plural = _("Profiles")

    def __str__(self):
        return self.full_name
 