from django import forms
from core.forms import SearchForm
class LoginForm(forms.Form):
    username=forms.CharField(max_length=50,required=True)
    password=forms.CharField(max_length=50,required=True)
    
class ChangePersonImageForm(forms.Form):
    person_id=forms.IntegerField(required=False)

 
class AddProfileForm(forms.Form):
    first_name=forms.CharField(max_length=11,required=False)
    last_name=forms.CharField(max_length=11,required=False)


class SelectUserForm(forms.Form):
    user_id=forms.IntegerField(required=False)


class SelectPersonForm(forms.Form):
    person_id=forms.IntegerField(required=False)

class AddPersonForm(forms.Form):
    user_id=forms.IntegerField(required=False)
    prefix=forms.CharField(max_length=11,required=False)
    title=forms.CharField(max_length=50,required=False)
    first_name=forms.CharField(max_length=50,required=False)
    last_name=forms.CharField(max_length=50,required=False)
    mobile=forms.CharField(max_length=50,required=False)
    email=forms.CharField(max_length=50,required=False)
    bio=forms.CharField(max_length=2000,required=False)
    address=forms.CharField(max_length=200,required=False)
    type=forms.CharField(max_length=11,required=False)
    type2=forms.CharField(max_length=11,required=False)
    economic_no=forms.CharField(max_length=50,required=False)
    melli_code=forms.CharField(max_length=20,required=False)
    postal_code=forms.CharField(max_length=20,required=False)
    tel=forms.CharField(max_length=50,required=False)
 