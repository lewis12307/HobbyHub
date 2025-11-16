from django import forms

class SignUpForm(forms.Form):
     first_name = forms.CharField(label="First Name", max_length=255, strip=True)
     last_name = forms.CharField(label="Last Name", max_length=255, strip=True)
     username = forms.CharField(label="Username", max_length=255, strip=True)
     password = forms.CharField(label="Password", max_length=255, strip=True)    
     bio = forms.CharField(label="Bio", required=False, strip=True, empty_value=None)
     profile_picture = forms.ImageField(label="Profile Picture", required=False, empty_value=None)