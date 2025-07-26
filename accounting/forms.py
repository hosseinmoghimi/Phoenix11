
from django import forms
from utility.forms import SearchForm
class GetInvoiceLineItemUnitsForm(forms.Form):
    invoice_line_item_id=forms.IntegerField( required=True)


class EditFinancialEventForm(forms.Form):
    title=forms.CharField( required=True,max_length=100)
    financial_event_id=forms.IntegerField(required=True)
    discount_percentage=forms.IntegerField(required=False)
    tax_percentage=forms.IntegerField(required=False)
    shipping_fee=forms.IntegerField(required=False)
    amount=forms.IntegerField(required=False)
    event_datetime=forms.CharField(max_length=50, required=False)
    payment_method=forms.CharField(max_length=50, required=False)
    bedehkar_id=forms.IntegerField(required=False)
    bestankar_id=forms.IntegerField(required=False)
    description=forms.CharField(max_length=1000,required=False)

class EditFinancialDocumentForm(forms.Form):
    financial_document_id=forms.IntegerField( required=True)
    title=forms.CharField( required=True,max_length=100)
    status=forms.CharField(max_length=50, required=False)


class AddBrandForm(forms.Form):
    name=forms.CharField( required=True,max_length=100)



class AddAssetForm(forms.Form):
    title=forms.CharField( required=True,max_length=100)
    owner_id=forms.IntegerField(required=False)

class AddAccountForm(forms.Form):
    parent_code=forms.IntegerField( required=False)
    parent_id=forms.IntegerField( required=False)
    priority=forms.IntegerField( required=False)
    title=forms.CharField( max_length=100, required=False)
    code=forms.CharField( max_length=100, required=False)
    color=forms.CharField( max_length=100, required=False)
    nature=forms.CharField( max_length=100, required=False)


class AddPersonAccountForm(AddAccountForm):
    person_id=forms.IntegerField(required=True)
    person_category_id=forms.IntegerField(required=True)
    
    
class AddInvoiceLineItemUnitForm(forms.Form):
    invoice_line_item_id=forms.IntegerField(required=True)
    unit_name=forms.CharField(max_length=100, required=True)
    unit_price=forms.IntegerField(required=True)
    coef=forms.FloatField(required=True)
    default=forms.BooleanField(required=False)
 

class GetReportForm(forms.Form):
    account_id=forms.IntegerField(required=False)
    amount=forms.IntegerField(required=False)
    search_for=forms.CharField( max_length=100, required=False)
    start_date=forms.CharField( max_length=100, required=False)
    end_date=forms.CharField( max_length=100, required=False)


class SelectFinancialDocumentForm(forms.Form):
    accounting_document_id=forms.IntegerField(required=True)


class RemoveAccountFromPersonForm(forms.Form):
    person_category_id=forms.IntegerField(required=True)
    person_id=forms.IntegerField(required=True)


class SetParentCodeForm(forms.Form):
    account_code=forms.CharField(max_length=100, required=True)
    parent_code=forms.CharField(max_length=100, required=True)
    

class AddInvoiceLineItemForm(forms.Form):
    priority=forms.IntegerField( required=False)
    title=forms.CharField( max_length=100, required=True)
    barcode=forms.CharField( max_length=100, required=False) 
    unit_price=forms.IntegerField( required=False)
    unit_name=forms.CharField( max_length=100, required=False) 
    coef=forms.IntegerField( required=False)
    category_id=forms.IntegerField( required=False)


class AddProductForm(AddInvoiceLineItemForm):
    barcode=forms.CharField( max_length=100, required=False) 
    brand_id=forms.IntegerField( required=False)
    model=forms.CharField( max_length=100, required=False) 


class AddServiceForm(AddInvoiceLineItemForm):
    pass


class AddProductToCategoryForm(forms.Form):
    product_id=forms.IntegerField( required=True)
    category_id=forms.IntegerField( required=True)


class AddCategoryForm(forms.Form):
    title=forms.CharField( max_length=100, required=True)
    parent_id=forms.IntegerField(required=False)
    priority=forms.IntegerField(required=False)
    color=forms.CharField( max_length=100, required=False) 
 

class AddAccountToPersonForm(forms.Form):
    person_category_id=forms.IntegerField(required=True)
    person_id=forms.IntegerField(required=True)

    
class AddPersonCategoryForm(forms.Form):
    title=forms.CharField(max_length=100, required=True)
    account_code=forms.IntegerField(required=True)

 
class AddProductSpecificationForm(forms.Form):
    priority=forms.IntegerField(required=False)
    product_id=forms.IntegerField(required=True)
    super_name=forms.CharField(max_length=100, required=False)
    name=forms.CharField(max_length=100, required=True)
    value=forms.CharField(max_length=100, required=True)


class AddFinancialDocumentLineForm(forms.Form):
    account_id=forms.IntegerField(required=False)
    account_code=forms.CharField(max_length=100, required=True)
    title=forms.CharField(max_length=100, required=True)
    bedehkar=forms.IntegerField(required=True)
    bestankar=forms.IntegerField(required=True)
    financial_document_id=forms.IntegerField(required=True)
    financial_document_title=forms.CharField(max_length=20, required=False)
    financial_event_id=forms.IntegerField(required=True)
    persian_date_time=forms.CharField(max_length=20, required=False)
    date_time=forms.CharField(max_length=30, required=False)


class SelectFinancialEventForm(forms.Form):
    financial_event_id=forms.IntegerField(required=True)
     

class SelectFinancialDocumentForm(forms.Form):
    financial_document_id=forms.IntegerField(required=True)
     

class SetAccountPriorityForm(forms.Form):
    account_id=forms.IntegerField(required=True)
    priority=forms.IntegerField(required=True)


class AddFinancialDocumentForm(forms.Form):
    title=forms.CharField(max_length=100, required=False)


class AddFinancialEventForm(forms.Form):
    title=forms.CharField(max_length=100, required=True)
    event_datetime=forms.CharField(max_length=50, required=True)
    bedehkar_id=forms.IntegerField(required=True)
    bestankar_id=forms.IntegerField(required=True)
    amount=forms.IntegerField(required=True)
    payment_method=forms.CharField(max_length=100,required=False)
    description=forms.CharField(max_length=1000,required=False)
    shipping_fee=forms.IntegerField(required=False)

class AddInvoiceForm(AddFinancialEventForm):
    pass


class AddCostAccountForm(AddAccountForm):
    pass


class AddTaxAccountForm(AddAccountForm):
    pass


class AddBankForm(forms.Form):
    name=forms.CharField(max_length=100, required=True)


class AddBankAccountForm(forms.Form):
    parent_code=forms.CharField(max_length=100, required=True)
    title=forms.CharField(max_length=100, required=True)
    person_id=forms.IntegerField(required=True)
    bank_id=forms.IntegerField(required=True)
    code=forms.CharField(max_length=50, required=False)
    shaba_no=forms.CharField(max_length=50, required=False)
    account_no=forms.CharField(max_length=50, required=False)
    card_no=forms.CharField(max_length=20, required=False)


class ImportProductsFromExcelForm(forms.Form):
    is_open=forms.BooleanField(required=False)
    count=forms.IntegerField(required=True)


class ImportFromExcelForm(forms.Form):
    is_open=forms.BooleanField(required=False)
    count=forms.IntegerField(required=True)


class ImportServicesFromExcelForm(forms.Form):
    is_open=forms.BooleanField(required=False)
    count=forms.IntegerField(required=True)

    
class AddFinancialYearForm(forms.Form):
    name=forms.CharField(max_length=100, required=True)
    start_date=forms.CharField(max_length=50, required=True)
    end_date=forms.CharField(max_length=50, required=True)
    description=forms.CharField(max_length=1000,required=False)
    status=forms.CharField(max_length=50,required=False)


class AddEventFinancialDocumentLineForm(forms.Form):
    accounting_document_id=forms.IntegerField(required=True)
    accounting_document_title=forms.CharField(max_length=200,required=True)
    date_time=forms.CharField(max_length=50,required=True)
    account_code=forms.CharField(max_length=50,required=True)
    bestankar=forms.IntegerField(required=True)
    bedehkar=forms.IntegerField(required=True)
    financial_event_id=forms.IntegerField(required=False)
    

class AddInvoiceLineForm(forms.Form):
    invoice_line_item_id=forms.IntegerField(required=True)
    invoice_id=forms.IntegerField(required=True)
    discount_percentage=forms.IntegerField(required=False)
    quantity=forms.IntegerField(required=True)
    unit_price=forms.IntegerField(required=True)
    coef=forms.IntegerField(required=False)
    save=forms.BooleanField(required=False)
    unit_name=forms.CharField(max_length=100, required=True)
    default=forms.BooleanField(required=False)


class SearchInvoiceLineItemForm(forms.Form):
    search_for=forms.CharField(max_length=100, required=False)
    title=forms.CharField(max_length=100, required=False)
    barcode=forms.CharField(max_length=100, required=False)
    code=forms.CharField(max_length=100, required=False)


class SelectPersonAccountForm(forms.Form):
    pk=forms.IntegerField(required=False)
    person_account_id=forms.IntegerField(required=False)
    id=forms.IntegerField(required=False)
    code=forms.CharField(max_length=100, required=False)
    title=forms.CharField(max_length=100, required=False)


class SelectAccountForm(forms.Form):
    pk=forms.IntegerField(required=False)
    id=forms.IntegerField(required=False)
    code=forms.CharField(max_length=100, required=False)
    title=forms.CharField(max_length=100, required=False)


class SearchAccountsForm(forms.Form): 
    search_for=forms.CharField(max_length=100, required=True)


class AddCostForm(AddFinancialEventForm):
    priority=forms.IntegerField(required=False)


class AddTaxForm(AddFinancialEventForm):
    priority=forms.IntegerField(required=False)
