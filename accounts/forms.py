from .models import CustomUser
from django import forms


class MyUserCreationForm(forms.ModelForm):
    confirm_password = forms.CharField(label="Password confirmation", widget=forms.PasswordInput)
    class Meta:
        model = CustomUser
        fields = ['mobile', 'first_name', 'last_name', 'password']
    

class ConfirmForm(forms.Form):
    confirm_code = forms.CharField(max_length=5)
    

class LoginForm(forms.Form):
        mobile = forms.CharField(max_length=11)
        password = forms.CharField(label="Password", widget=forms.PasswordInput)

        
class ResetPasswordForm(forms.Form):

    password1 = forms.CharField(label="New Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput)
        
class MobileForm(forms.Form):
     mobile = forms.CharField(label="Mobile")