
import re
from django import forms
from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import UserCreationForm
from tasks.forms import Style_Form_Mixins
from django.contrib.auth.forms import AuthenticationForm 

class Register_form(UserCreationForm):
    class Meta:
        model = User 
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)

        for fieldname in ['username', 'password1', 'password2']:
            self.fields[ fieldname ].field_error = None

        self.fields['username'].help_text = 'Who are you'


class CustomRegisterForm(Style_Form_Mixins, forms.ModelForm):

    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

    # For Field Errors 
    def clean_password1(self):

        password1 = self.cleaned_data.get('password1')
        pattern = "^.*(?=.{8,})(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[@#$%^&+=]).*$"
        errors = []

        if len(password1) < 8:
            errors.append("password mast have length 8")
        if not re.findall(pattern, password1):
            errors.append("password mast have A-Z, a-z, 0-9, @#&%^$")
        if errors:
            raise forms.ValidationError(errors)
        
        return password1


    # For Non Field Errors 
    def clean(self):
        cleaned_data = super().clean()
        pass1 = cleaned_data.get('password1')
        pass2 = cleaned_data.get('password2')

        if pass1 != pass2:
            raise forms.ValidationError("password don't matched")
        
        return cleaned_data
    

    def clean_email(self):
        email_from_user = self.cleaned_data.get('email')
        email_from_db = User.objects.filter(email = email_from_user).exists()

        if email_from_db:
            raise forms.ValidationError("this email already exist chose another")
        
        return email_from_user

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])  # Hash the password
        if commit:
            user.save()
        return user


class CustomLoginForm(Style_Form_Mixins, AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class assignRoleForm(Style_Form_Mixins, forms.Form):
    role = forms.ModelChoiceField(
        queryset=Group.objects.all(),
        empty_label="Select a Role"
    )
