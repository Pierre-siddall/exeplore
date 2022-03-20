"""This file represents all the forms in the main app"""
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from users.models import Player
from visits.models import Location, Badge
User = get_user_model()

class SignUpForm(UserCreationForm):
    """This represents the User registration form"""
    #adds help text to fields
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254,
    help_text='Required. Input a valid UoE email address.')
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )

class PlayerForm(forms.ModelForm):
    """This class represents the Player registration form, an extension of the Signupform"""
    class Meta:
        model = Player
        #imports the signupform, excludes the forms that the user doesn't need to see
        #Doesn't use explicit fields as there's no fields for the player form to have that
        #the sign up form doesn't have, and that can be changed upon registration
        exclude = ('score', 'user', 'badges', 'visits' )

class AddLocationForm(forms.ModelForm):
    """ This class represents the new location form """
    icon = forms.FileField(required=False) # an icon image is not required
    class Meta:
        model = Location
        fields = ('location_name', 'latitude', 'longitude', 'point_value', 'icon')

class AddBadgeForm(forms.ModelForm):
    """ This class represents the new badge form """
    icon = forms.FileField(required=False) # an icon image is not required
    class Meta:
        model = Badge
        fields = ('badge_name', 'description', 'tier', 'icon')

