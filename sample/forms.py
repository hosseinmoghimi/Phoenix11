from accounting.forms import forms

class AddSampleForm(forms.Form):
    title=forms.CharField(max_length=100,required=True) 
 