from django.contrib import admin
from .models import Account,FinancialEvent,EventCategory,InvoiceLineItemUnit,InvoiceLineItem,Service,Product


admin.site.register(Account)
admin.site.register(FinancialEvent)
admin.site.register(EventCategory)
admin.site.register(InvoiceLineItemUnit)
admin.site.register(InvoiceLineItem)
admin.site.register(Product)
admin.site.register(Service)