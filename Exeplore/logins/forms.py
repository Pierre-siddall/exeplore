from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

# This overwrites django's form
class registerForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Register:
        model = User
        fields = ("username", "fname", "lname","email", "password")