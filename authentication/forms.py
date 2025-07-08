from django import forms

class LoginForm(forms.Form):
    username=forms.CharField(max_length=50,required=True)
    password=forms.CharField(max_length=50,required=True)


class AddPersonForm(forms.Form):
    profile_id=forms.IntegerField(required=False)
    prefix=forms.CharField(max_length=11,required=False)
    first_name=forms.CharField(max_length=50,required=False)
    last_name=forms.CharField(max_length=50,required=True)
    mobile=forms.CharField(max_length=50,required=False)
    email=forms.CharField(max_length=50,required=False)
    bio=forms.CharField(max_length=2000,required=False)
    address=forms.CharField(max_length=100,required=False)
    type=forms.CharField(max_length=11,required=False)
    type2=forms.CharField(max_length=11,required=False)
    melli_code=forms.CharField(max_length=11,required=False)
    tel=forms.CharField(max_length=11,required=False)
 