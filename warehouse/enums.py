from django.utils.translation import gettext as _
from django.db.models import TextChoices
from accounting.enums import UnitNameEnum

class WareHouseSheetDirectionEnum(TextChoices):
    IN='ورود',_('ورود')
    OUT='خروج',_('خروج')