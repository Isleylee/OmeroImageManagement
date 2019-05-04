from django import forms
from captcha.fields import CaptchaField


# All the forms should be added here
class UserForm(forms.Form):
    username = forms.CharField(label="User name", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label="Password", max_length=256, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    captcha = CaptchaField(label='Validation code')

class RegisterForm(forms.Form):
    gender = (
        ('male', "M"),
        ('female', "F"),
    )
    username = forms.CharField(label="User name", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label="Password", max_length=256, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label="Confirm password", max_length=256, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label="Email address", widget=forms.EmailInput(attrs={'class': 'form-control'}))
    sex = forms.ChoiceField(label='Sex', choices=gender)
    captcha = CaptchaField(label='Validation code', error_messages={'invalid':'Incorrect code!'})

class ForgetForm(forms.Form):
    email = forms.EmailField(required=True)
    captcha = CaptchaField(label='Validation code', error_messages={'invalid':'Incorrect code!'})

class ResetForm(forms.Form):
    newpwd1 = forms.CharField(required=True,min_length=6,error_messages={'required': 'Should not be empty.', 'min_length': "At lease 6"})
    newpwd2 = forms.CharField(required=True, min_length=6, error_messages={'required': 'Should not be empty.', 'min_length': "At lease 6"})


# Uploaded image form
class ImageForm(forms.Form):
    image_date = forms.CharField(label="Image Date", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control'}))
    sex = forms.CharField(label="Sex", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control'}))
    strain = forms.CharField(label="Acquisition", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control'}))



