from django import forms
 
class AddVehicleForm(forms.Form):
    title=forms.CharField( max_length=100, required=True)
 