from django.contrib import admin
from .models import WareHouse,WareHouseMaterialSheet,MaterialTerminal,MaterialPort 

admin.site.register(WareHouse)
admin.site.register(WareHouseMaterialSheet)
admin.site.register(MaterialTerminal)
admin.site.register(MaterialPort)