from accounting.forms import forms

class AddTaskForm(forms.Form):
    title=forms.CharField(max_length=100,required=True) 
 
class AddAppointmentForm(AddTaskForm):
    persons_to_meet_ids=forms.IntegerField(required=False)
 