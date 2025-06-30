from django.utils.translation import gettext as _

from django.db.models import TextChoices




class ProjectTypeEnum(TextChoices):
    TYPE_A="تایپ A",_("تایپ A")
    TYPE_B="تایپ B",_("تایپ B")






class ProjectStatusEnum(TextChoices):
    DRAFT="پیش نویس",_("پیش نویس")
    STARTED="شروع شده",_("شروع شده")
    IN_PROGRESS="در جریان",_("در جریان")
    FINISHED="پایان یافته",_("پایان یافته") 

class TicketTypeEnum(TextChoices):
    TYPE_A="تایپ A",_("تایپ A")
    TYPE_B="تایپ B",_("تایپ B")
    TYPE_C="تایپ C",_("تایپ C")



class TicketStatusEnum(TextChoices):
    STARTED="شروع شده",_("شروع شده")
    IN_PROGRESS="در جریان",_("در جریان")
    FINISHED="پایان یافته",_("پایان یافته") 

