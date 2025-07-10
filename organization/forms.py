from accounting.forms import AddProductForm,forms
 
class AddOrganizationUnitForm(forms.Form):
    title=forms.CharField(max_length=50,required=True)
    account_id=forms.IntegerField(required=True)
    
 
class AddEmployeeForm(forms.Form):
    job_title=forms.CharField(max_length=50,required=True)
    organization_unit_id=forms.IntegerField(required=True)
    person_id=forms.IntegerField(required=True)
    
 
class SelectOrganizationUnitForm(forms.Form):
    organization_unit_id=forms.IntegerField(required=True)
    
 
class SelectEmployeeForm(forms.Form):
    employee_id=forms.IntegerField(required=True)
    
 