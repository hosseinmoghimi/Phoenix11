from django.contrib import admin
from .models import WareHouse,WareHouseSheet,MaterialPort,WareHouseSheetSignature,WareHouseSheetLabel

admin.site.register(WareHouse)
admin.site.register(WareHouseSheet)
admin.site.register(MaterialPort)
admin.site.register(WareHouseSheetSignature)
admin.site.register(WareHouseSheetLabel)