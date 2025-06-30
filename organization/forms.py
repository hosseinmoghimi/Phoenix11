from accounting.forms import AddProductForm,forms
 
class AddOrganizationForm(forms.Form):
    title=forms.CharField(max_length=50,required=True)
    event_datetime=forms.CharField(max_length=50,required=False)
    
 