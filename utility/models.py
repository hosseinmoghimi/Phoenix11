from django.db import models
from django.utils.translation import gettext as _
  
from phoenix.settings import ADMIN_URL,STATIC_URL,MEDIA_URL
from django.shortcuts import reverse 
from .calendar import PersianCalendar
from .apps import APP_NAME


class DateHelper():
    def persian_start_date(self):
        return PersianCalendar().from_gregorian(self.start_date)
    def persian_end_date(self):
        return PersianCalendar().from_gregorian(self.end_date)
    def persian_date(self):
        return PersianCalendar().from_gregorian(self.date)
    def persian_date_added(self):
        return PersianCalendar().from_gregorian(self.date_added)
    def persian_date_added(self):
        return PersianCalendar().from_gregorian(self.date_added)
    def persian_date_created(self):
        return PersianCalendar().from_gregorian(self.date_created)
    def persian_date_modified(self):
        return PersianCalendar().from_gregorian(self.date_modified)


class DateTimeHelper(DateHelper):
    def persian_start_datetime(self):
        return PersianCalendar().from_gregorian(self.start_datetime)
    def persian_end_datetime(self):
        return PersianCalendar().from_gregorian(self.end_datetime)
    def persian_datetime(self):
        return PersianCalendar().from_gregorian(self.datetime)
    def persian_transaction_datetime(self):
        return PersianCalendar().from_gregorian(self.transaction_datetime)
    def persian_print_datetime(self):
        return PersianCalendar().from_gregorian(self.print_datetime)
    def persian_datetime_added(self):
        return PersianCalendar().from_gregorian(self.datetime_added) 
    def persian_date_added(self):
        return PersianCalendar().from_gregorian(self.date_added) 
    def persian_document_datetime(self):
        return PersianCalendar().from_gregorian(self.document_datetime)
    def persian_event_datetime(self):
        return PersianCalendar().from_gregorian(self.event_datetime)

class ImageHelper:
    @property
    def image(self):
        image=""
        try:
            sss=self.image_origin
        except:
            return self.thumbnail

        if self.image_origin is None or str(self.image_origin)=="":
            try:
                image= f"{STATIC_URL}{self.app_name}/img/pages/image/{self.class_name}.png/"
            except:
                pass
        else:
            image= f"{MEDIA_URL}{self.image_origin}"

        return image
    @property
    def thumbnail(self):
        thumbnail=""
        if self.thumbnail_origin is None or str(self.thumbnail_origin)=="":
            try:
                thumbnail= f"{STATIC_URL}{self.app_name}/img/pages/thumbnail/{self.class_name}.png/"
            except:
                pass
        else:
            thumbnail= f"{MEDIA_URL}{self.thumbnail_origin}"

        return thumbnail

    @property
    def header(self):
        header=""
        if self.header_origin is None or str(self.header_origin)=="":
            try:
                header= f"{STATIC_URL}{self.app_name}/img/pages/thumbnail/{self.class_name}.png/"
            except:
                pass
        else:
            header= f"{MEDIA_URL}{self.header_origin}"

        return header


        
    @property
    def logo(self):
        logo=""
        if self.logo_origin is None or str(self.logo_origin)=="":
            try:
                logo= f"{STATIC_URL}{self.app_name}/img/pages/thumbnail/{self.class_name}.png/"
            except:
                pass
        else:
            logo= f"{MEDIA_URL}{self.logo_origin}"

        return logo



class LinkHelper():
    def get_edit_url(self):
        return f"{ADMIN_URL}{self.app_name}/{self.class_name}/{self.pk}/change/"
    def get_absolute_url(self):
        return reverse(f"{self.app_name}:{self.class_name}",kwargs={'pk':self.pk})
    def get_delete_url(self):
        return f"{ADMIN_URL}{self.app_name}/{self.class_name}/{self.pk}/delete/"
        
    def get_edit_url_admin(self):
        return f'{ADMIN_URL}{self.app_name}/{self.class_name}/{self.pk}/change/'


    def get_edit_btn(self):
        return f"""
          <a target="_blank" title="ویرایش" href="{self.get_edit_url()}"><i class="fa fa-edit text-warning"></i></a>
        """
    def get_delete_btn(self):
        return f"""
          <a target="_blank" title="حذف" href="{self.get_delete_url()}"><i class="fa fa-trash text-danger"></i></a>
        """


 

 

class Parameter(models.Model):
    app_name = models.CharField(_("app_name"), max_length=50)
    name = models.CharField(_("نام پارامتر (تغییر ندهید)"), max_length=50)
    origin_value = models.CharField(
        _("مقدار پارامتر"), null=True, blank=True, max_length=50000)
    class_name = "parameter"

    @property
    def value(self):
        if self.origin_value is None:
            return ''
        return self.origin_value
    
    
    @property
    def int_value(self):
        if self.origin_value is None:
            return 0
        return int(self.origin_value)


    @property
    def boolean_value(self):
        if self.origin_value is None:
            return False
        if self.origin_value == 'True':
            return True
        if self.origin_value == '1':
            return True
        if self.origin_value == 'true':
            return True
        if self.origin_value == 'بله':
            return True
        if self.origin_value == 'درست':
            return True
        if self.origin_value == 'آری':
            return True
        return False

    class Meta:
        verbose_name = _("Parameter")
        verbose_name_plural = _("Parameters")

    def __str__(self):
        return self.app_name+":"+self.name

    def get_edit_url(self):
        return f"{ADMIN_URL}{APP_NAME}/parameter/{self.pk}/change/"

    def get_delete_url(self):
        return f"{ADMIN_URL}{APP_NAME}/parameter/{self.pk}/delete/"

    def get_edit_btn(self):
        return f"""
            <a title="ویرایش" target="_blank" href="{self.get_edit_url()}">
                <i class="fa fa-edit text-info mx-2"></i>
            </a>
        """


