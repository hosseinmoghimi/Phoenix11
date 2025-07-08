from accounting.forms import AddProductForm,forms

class AddSchoolForm(forms.Form):
    name=forms.CharField(max_length=50,required=True)
    account_id=forms.IntegerField(required=True)

class AddCourseForm(forms.Form):
    title=forms.CharField(max_length=50,required=True)
    event_datetime=forms.CharField(max_length=50,required=False)
    bestankar_id=forms.IntegerField(required=True)
    bedehkar_id=forms.IntegerField(required=True)

class AddCourseClassForm(forms.Form):
    title=forms.CharField(max_length=50,required=True)
    event_datetime=forms.CharField(max_length=50,required=False)

class AddStudentForm(forms.Form):
    title=forms.CharField(max_length=50,required=True)
    event_datetime=forms.CharField(max_length=50,required=False)