from accounting.forms import AddProductForm,forms
 
class AddProjectForm(forms.Form):
    title=forms.CharField(max_length=50,required=True)
    contractor_id=forms.IntegerField(required=True)
    employer_id=forms.IntegerField(required=True)
    percentage_completed=forms.IntegerField(required=True)
    event_datetime=forms.CharField(max_length=50,required=False)
    start_datetime=forms.CharField(max_length=50,required=False)
    end_datetime=forms.CharField(max_length=50,required=False)
    type=forms.CharField(max_length=50,required=False)
    weight=forms.IntegerField(required=False)
    
 