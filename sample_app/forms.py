from accounting.forms import forms

class AddSampleClassForm(forms.Form):
    title=forms.CharField(max_length=100,required=True) 
 