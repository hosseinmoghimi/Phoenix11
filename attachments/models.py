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
    




    
class Icon(models.Model,LinkHelper):
    title = models.CharField(_("title"), null=True, blank=True, max_length=300)
    icon_fa = models.CharField(
        _("icon fa"), null=True, blank=True, max_length=50)
    icon_material = models.CharField(
        _("material_icon"), null=True, blank=True, max_length=50)
    icon_svg = models.TextField(_("svg_icon"), null=True, blank=True)
    # profile = models.ForeignKey("authentication.profile", null=True,
                                # blank=True, verbose_name=_("profile"), on_delete=models.CASCADE)
    color = models.CharField(
        _("color"), choices=ColorEnum.choices, default=ColorEnum.PRIMARY, max_length=50)
    width = models.IntegerField(_("عرض آیکون"), null=True, blank=True)
    height = models.IntegerField(_("ارتفاع آیکون"), null=True, blank=True)
    priority = models.IntegerField(_("priority"), default=1000)
    image_origin = models.ImageField(_("تصویر آیکون"), upload_to=IMAGE_FOLDER+'Icon/',
                                     height_field=None, null=True, blank=True, width_field=None, max_length=None)
    class_name='icon'
    app_name=APP_NAME
    def get_icon_tag(self, icon_style='', color=None, no_color=False):

        if color is not None:
            self.color = color
        text_color = ''
        if not no_color and self.color is not None:
            text_color = 'text-'+self.color

        if self.image_origin is not None and self.image_origin:
            return f'<img src="{MEDIA_URL}{str(self.image_origin)}" alt="{self.title}" height="{self.height}" width="{self.width}">'

        if self.icon_material is not None and len(self.icon_material) > 0:
            return f'<i style="{icon_style}" class="{text_color} material-icons">{self.icon_material}</i>'

        if self.icon_fa is not None and len(self.icon_fa) > 0:
            return f'<i style="{icon_style}" class="{text_color} {self.icon_fa}"></i>'

        if self.icon_svg is not None and len(self.icon_svg) > 0:
            return f'{self.icon_svg}'
        if self.icon_svg is not None and len(self.icon_svg) > 0:
            return f'<span  style="{icon_style}" class="{text_color}">{self.icon_svg}</span>'
        return ''

    def get_icon_tag_pure(self, icon_style='', color=None, no_color=False):

        if color is not None:
            self.color = color
        text_color = ''
        if not no_color and self.color is not None:
            text_color = 'text-'+self.color

        if self.image_origin is not None and self.image_origin:
            return f'<img src="{MEDIA_URL}{str(self.image_origin)}" alt="{self.title}" height="{self.height}" width="{self.width}">'

        if self.icon_material is not None and len(self.icon_material) > 0:
            return f'<i style="{icon_style}" class="material-icons">{self.icon_material}</i>'

        if self.icon_fa is not None and len(self.icon_fa) > 0:
            return f'<i style="{icon_style}" class="{self.icon_fa}"></i>'

        if self.icon_svg is not None and len(self.icon_svg) > 0:
            return f'<span  style="{icon_style}" class="{text_color}">{self.icon_svg}</span>'
        return ''

    class Meta:
        verbose_name = _("Icon")
        verbose_name_plural = _("Icons")

    def __str__(self):
        return self.title


class Download(Icon):
    page = models.ForeignKey("core.page", verbose_name=_(
        "page"), on_delete=models.CASCADE)
    
    file = models.FileField(_("فایل ضمیمه"), null=True, blank=True,
                            upload_to=APP_NAME+'/downloads', storage=upload_storage, max_length=100)
    mirror_link = models.CharField(
        _('آدرس بیرونی'), null=True, blank=True, max_length=10000)
    date_added = models.DateTimeField(
        _("افزوده شده در"), auto_now=False, auto_now_add=True)
    date_updated = models.DateTimeField(
        _("اصلاح شده در"), auto_now_add=False, auto_now=True)
    download_counter = models.IntegerField(_("download_counter"), default=0)
    profiles = models.ManyToManyField(
        "authentication.profile", blank=True, related_name="profile_downloads", verbose_name=_("profiles"))
    is_open = models.BooleanField(_("is_open?"), default=False)
    profile = models.ForeignKey("authentication.Profile", null=True,
                                blank=True, verbose_name=_("profile"), on_delete=models.CASCADE)
    class_name='download'
    app_name=APP_NAME
    @property
    def get_download_url(self):
        if self.mirror_link and self.mirror_link is not None:
            return self.mirror_link
        if self.file:
            ss= reverse(APP_NAME+':download', kwargs={'pk': self.pk})
            return ss
        else:
            return ''

    @property
    def get_full_download_url(self):
        if self.mirror_link and self.mirror_link is not None:
            return self.mirror_link
        if self.file:
            ss= reverse(APP_NAME+':download', kwargs={'pk': self.pk})
            return FULL_SITE_URL[0:len(FULL_SITE_URL)-1]+ss
        else:
            return ''

          

    class Meta:
        verbose_name = _("Download")
        verbose_name_plural = _("Downloads")

    def __str__(self):
        return self.title


    def get_qrcode_url(self):
        if self.pk is None:
            super(Download,self).save()
        import os
        file_path = QRCODE_ROOT
        file_name=self.class_name+str(self.pk)+".svg"
        file_address=os.path.join(QRCODE_ROOT,file_name)
        if not os.path.exists(file_address):
            content=self.get_full_download_url
            generate_qrcode(content=content,file_name=file_name,file_address=file_address,file_path=file_path,)
        return f"{QRCODE_URL}{file_name}"
 

class Link(Icon,LinkHelper):
    page = models.ForeignKey("core.page", verbose_name=_(
        "page"), on_delete=models.CASCADE)
    
    url = models.CharField(_("url"), max_length=2000)
    new_tab=models.BooleanField(_("new_tab"),default=False)
    profile = models.ForeignKey("authentication.Profile", null=True,
                                blank=True, verbose_name=_("profile"), on_delete=models.CASCADE)
    class_name='link'
    app_name=APP_NAME
    class Meta:
        verbose_name = _("Link")
        verbose_name_plural = _("Links")

    def get_absolute_url(self):
        return reverse("Link_detail", kwargs={"pk": self.pk})

    def get_link_btn(self):
        target='target="_blank"' if self.new_tab else ''
        return f"""

            <a {target} class="btn btn-{self.color} " href="{self.url}">
            <span class="ml-2">
            {self.get_icon_tag_pure()}
            </span>
            {self.title}
            </a>
        """
    
    def get_qrcode_url(self):
        if self.pk is None:
            super(Link,self).save()
        import os
        file_path = QRCODE_ROOT
        file_name=self.class_name+str(self.pk)+".svg"
        file_address=os.path.join(QRCODE_ROOT,file_name)
        if not os.path.exists(file_address):
            content=self.url
            generate_qrcode(content=content,file_name=file_name,file_address=file_address,file_path=file_path,)
        return f"{QRCODE_URL}{file_name}"
 
 