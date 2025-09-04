from accounting.forms import forms,AddProductForm
 
class AddDrugForm(AddProductForm):
    pass


class AddDoctorForm(forms.Form):
    person_account_id=forms.IntegerField(required=True)


class AddPatientForm(forms.Form):
    person_account_id=forms.IntegerField(required=True)

class AddPrescriptionForm(AddProductForm):
    pass