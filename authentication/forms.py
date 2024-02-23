from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from .models import Profile

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class CheckCustomerForm(forms.Form):  #form for granting access to customer functions
        codeword = forms.CharField(max_length=16, label='codeword')


class UserNotificationForm(forms.Form):
        email1 = forms.CharField(max_length=100, label='email1')
        email1cd = forms.BooleanField(label='email1 enabler')
        email2 = forms.CharField(max_length=100, label='email2')
        email2cd = forms.BooleanField(label='email2 enabler')
        telegram1 = forms.CharField(max_length=250, label='telegram1')
        telegram1cd = forms.BooleanField(label='telegram1 enabler')
        telegram2 = forms.CharField(max_length=250, label='telegram2')
        telegram2cd = forms.BooleanField(label='telegram2 enabler')
