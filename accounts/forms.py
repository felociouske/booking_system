from django import forms 
from django.contrib.auth.forms import AuthenticationForm , UserCreationForm
from django.contrib.auth.models import User
from .models import Profile


class UserLogin(forms.Form):
    username = forms.CharField(label = "Enter Your email Address(Same as one used on admission)", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Student Email/Personal Email)"}))
    password = forms.CharField(label="Enter Your Registration Number in Capital Letters",widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': "Password"}),max_length=15,help_text="Insert Your correct Registration Number")

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if len(password) < 15:
            raise forms.ValidationError("Password exceeds the number of characters.")
        return password

class GenderSelectionForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['gender'].empty_label = "Choose your gender"

    class Meta:
        model = Profile 
        fields = ['gender']
        widgets = {
            'gender': forms.Select(attrs={'class': 'form-select'}),
        }


class Password_change_form(forms.Form):
    old_password = forms.CharField(label = "Current Password", widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': "Current Password"}))
    new_password1 = forms.CharField(label = "New Password", widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': "New Password"}))
    new_password2 = forms.CharField(label='Confirm New Password', widget=forms.PasswordInput(attrs={'placeholder': "Confirm New Password"}))

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user

    def clean_old_password(self):
        old_password = self.cleaned_data.get('old_password')
        if not self.user.check_password(old_password):
            raise forms.ValidationError("Old password is not correct")
        return old_password

    def clean(self):
        cleaned_data = super().clean()
        new1 = cleaned_data.get('new_password1')
        new2 = cleaned_data.get('new_password2')
        if new1 and new2 and new1 != new2:
            self.add_error('new_password2', 'The two new passwords do not match')
            return cleaned_data
           