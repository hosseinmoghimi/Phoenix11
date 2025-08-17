from accounting.forms import forms

class AddTrafficForm(forms.Form):
    title=forms.CharField(max_length=100,required=True) 
 