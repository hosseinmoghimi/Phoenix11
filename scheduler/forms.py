from accounting.forms import forms

class AddAppointmentForm(forms.Form):
    title=forms.CharField(max_length=100,required=True) 
 