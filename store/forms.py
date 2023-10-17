from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import *
from django.forms import ModelForm


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['phone', 'full_name', 'password1', 'password2']


class AddInstrumentForm(ModelForm):
    class Meta:
        # model = MusicalInstrument
        fields = '__all__'

