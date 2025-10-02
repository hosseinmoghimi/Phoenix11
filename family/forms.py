from accounting.forms import forms

class AddFamilyForm(forms.Form):
    title=forms.CharField(max_length=100,required=True) 
 