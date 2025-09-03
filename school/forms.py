from accounting.forms import AddProductForm,forms

class AddSchoolForm(forms.Form):
    name=forms.CharField(max_length=100,required=True) 
    person_account_id=forms.IntegerField(required=True)

class AddCourseForm(forms.Form):
    title=forms.CharField(max_length=100,required=True) 

class AddCourseClassForm(forms.Form): 
    room=forms.CharField(max_length=50,required=False)
    school_id=forms.IntegerField(required=True)
    course_id=forms.IntegerField(required=True)

class AddStudentForm(forms.Form):
    person_account_id=forms.IntegerField(required=True)

class AddSessionForm(forms.Form):
    title=forms.CharField(max_length=50,required=True)

   
class AddStudentInSessionForm(forms.Form):
    session_id=forms.IntegerField(required=True)
    student_id=forms.IntegerField(required=True)
    status=forms.CharField(max_length=50,required=True)
    score=forms.IntegerField(required=False)
    description=forms.CharField(max_length=5000,required=False)
 
class AddMajorForm(forms.Form):
    title=forms.CharField(max_length=50,required=True)

class AddTeacherForm(forms.Form):
    person_account_id=forms.IntegerField(required=True)