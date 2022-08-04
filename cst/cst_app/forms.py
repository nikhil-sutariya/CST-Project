from django.contrib.auth.forms import UserCreationForm
from .models import *
from django.forms import ModelForm

class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone', 'role', 'password1', 'password2']

class CreateAgency(ModelForm):
    class Meta:
        model = Agency
        fields = ['agency_name', 'address', 'work_phone']

class SendInvite(ModelForm):
    class Meta:
        model = Customer
        fields = ['email']