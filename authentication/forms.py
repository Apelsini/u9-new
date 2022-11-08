from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class CheckCustomerForm(forms.Form):  #form for granting access to customer functions
        codeword = forms.CharField(max_length=16, label='codeword')
