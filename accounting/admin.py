from django.contrib import admin
from .models import PersonAccount,PersonAccountCategory,Account,FinancialEvent,InvoiceLineItemUnit,InvoiceLineItem,Service,Product,Invoice,InvoiceLine,Person


admin.site.register(Account)
admin.site.register(FinancialEvent)
admin.site.register(InvoiceLineItemUnit)
admin.site.register(InvoiceLineItem)
admin.site.register(Product)
admin.site.register(Service)
admin.site.register(Person)
admin.site.register(PersonAccountCategory)
admin.site.register(PersonAccount)
admin.site.register(InvoiceLine)
admin.site.register(Invoice)