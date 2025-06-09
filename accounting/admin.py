from django.contrib import admin
from .models import PersonAccount,PersonAccountCategory,Account,FinancialEvent,InvoiceLineItemUnit,InvoiceLineItem,Service,Product,Invoice,InvoiceLine,Person,Bank,BankAccount,PersonCategory


admin.site.register(Account)
admin.site.register(Bank)
admin.site.register(BankAccount)
admin.site.register(FinancialEvent)
admin.site.register(Invoice)
admin.site.register(InvoiceLine)
admin.site.register(InvoiceLineItem)
admin.site.register(InvoiceLineItemUnit)
admin.site.register(Person)
admin.site.register(PersonAccount)
admin.site.register(PersonAccountCategory)
admin.site.register(PersonCategory)
admin.site.register(Product)
admin.site.register(Service)