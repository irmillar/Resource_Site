from django import forms
from .models import Resource, UserProfileInfo
from django.contrib.auth.models import User


class NewResourceForm(forms.ModelForm):
    class Meta:
        model = Resource
        fields = "__all__"

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ('username', 'email', 'password')

class UserProfileInfoForm(forms.ModelForm):
    class Meta:
        model = UserProfileInfo
        exclude = ('user',)


class UserLoginForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ('username', 'password')
