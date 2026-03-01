from django.contrib.auth.forms import PasswordChangeForm, PasswordResetForm, SetPasswordForm, UserCreationForm
from .models import STATE_CHOICES, Customer, User
from django import forms

class CustomUserForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter user Name'}))
    email = forms.CharField(widget=forms.EmailInput(attrs={'class':'form-control','placeholder':'Enter Email address'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Enter your Password'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Enter confirm Password'}))
    class Meta:
        model=User
        fields=['username','email','password1','password2']

class CustomerProfileForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Name'}))
    locality = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Locality'}))
    city = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter City'}))
    zipcode = forms.CharField(widget=forms.NumberInput(attrs={'class':'form-control','placeholder':'Enter Zipcode'}))
    state = forms.CharField(widget=forms.Select(attrs={'class':'form-control'},choices=STATE_CHOICES))
    mobile = forms.CharField(widget=forms.NumberInput(attrs={'class':'form-control','placeholder':'Enter Mobile Number'}))
    class Meta:
        model=Customer
        fields=['name','locality','city','mobile','zipcode','state']

class MyPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Enter Old Password'}))
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Enter New Password'}))
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Confirm New Password'}))
    class Meta:
        model=User
        fields=['old_password','new_password1','new_password2']

class MyPasswordResetForm(PasswordResetForm):
    email = forms.CharField(widget=forms.EmailInput(attrs={'class':'form-control','placeholder':'Enter Your Email'}))
    class Meta:
        model=User
        fields=['email']

class MysetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(label='New Password',widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Enter New Password'}))
    new_password2 = forms.CharField(label='Confirm New password',widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Confirm New Password'}))
    class Meta:
        model=User
        fields=['new_password1','new_password2']
    