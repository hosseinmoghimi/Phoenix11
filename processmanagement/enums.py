
from django.db.models import TextChoices
from django.utils.translation import gettext as _
class OperationEnum(TextChoices):
    ADD="add",_("add")
    CHANGE="change",_("change")
    VIEW="view",_("view")
    DELETE="delete",_("delete")
class AppNameEnum(TextChoices):
    accounting="حسابداری",_("حسابداری")
    projectmanagement="مدیریت پروژه",_("مدیریت پروژه")