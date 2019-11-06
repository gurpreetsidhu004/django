from django import forms
from .models import Data_record
from django.contrib.auth.models import User


class BookForm(forms.ModelForm):
    class Meta:
        model = Data_record
        fields = ('title', 'categories', 'feature_image', 'complete_tags', 'iframe' ,'mobiledoc')


class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_pass = forms.CharField(widget=forms.PasswordInput())
    def clean(self):
        clean_data = super().clean()
        pwd = clean_data['password']
        cnfmpwd = clean_data['confirm_pass']
        if pwd != cnfmpwd:
            raise forms.ValidationError("Password does not match")
    class Meta():
        model = User
        fields =('first_name', 'last_name', 'username', 'email', 'password')
