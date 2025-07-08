
from django.utils.translation import gettext as _
from utility.enums import UnitNameEnum,TextChoices
 
class PersonType2Enum(TextChoices):
    HAGHIGHI='حقیقی',_('حقیقی')
    HOGHUGHI='حقوقی',_('حقوقی')




class PersonTypeEnum(TextChoices):
    CUSTOMER="مشتری",_("مشتری")
    HOGHUGHI="حقوقی",_("حقوقی")
    PERSONNEL="پرسنل",_("پرسنل")
    FREE="بدون کنترل",_("بدون کنترل")

