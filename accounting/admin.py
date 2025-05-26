from django.contrib import admin
from .models import Account,FinancialEvent,EventCategory


admin.site.register(Account)
admin.site.register(FinancialEvent)
admin.site.register(EventCategory)