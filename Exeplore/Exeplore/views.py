"""This file houses the views for the app, including the User registration,
login, and rendering of other pages"""
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate, get_user_model
from django.contrib.auth.models import Group, User

from visits.models import Badge, Location
from users.models import Player, EarnedBadge

from .forms import SignUpForm, PlayerForm
def register(request):
    """This method registers a user by using the SignUpForm, and associates a
    Player with them"""
    if request.method == "POST":
        form = SignUpForm(request.POST)
        player_form = PlayerForm(request.POST)
        #if the error is with the user's entries
        if form.is_valid():
            #if there's some error with creating the Player to go with the User
            if player_form.is_valid():
                user =form.save()
                #add the new user to the admin group Player
                group  = Group.objects.get(name = 'Player')
                user.groups.add(group)
                messages.success(request, "Registration successful.")
                return redirect('/home/') # redirects to the home page
            else:
                messages.error(request, player_form.errors)
                messages.error(request, "invalid - user")
        else:
            messages.error(request, form.errors)
            messages.error(request, "Invalid form input - original")
    form = SignUpForm()
    player_form = PlayerForm()
    return render(request=request, template_name="registration/register.html",
    context={"register_form": form, "player_form":form})

def login_view(request):
    """This method defines the login functionality, using the Authentication Form"""
    if request.method == "POST":
        auth_form = AuthenticationForm(request, data=request.POST)
        if auth_form.is_valid():
            username = auth_form.cleaned_data.get('username')
            password = auth_form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, "logged in as", username, ".")
                request.session['username'] = username
                return redirect('/home/')
            else:
                messages.error(request,"Invalid username and/or password")
        else:
            messages.error(request,"Invalid username and/or password")
    auth_form = AuthenticationForm()
    return render(request=request, template_name="registration/login.html",
    context={"login_form": auth_form})


def home(request):
    """This function renders the home page"""
    return render(request=request, template_name="registration/home.html")

def splash(request):
    """This function renders the splash page"""
    return render(request=request, template_name="registration/splash.html")

def settings(request):
    """This function renders the settings page"""
    name = request.session.get('username')
    user = User.objects.get(username=name)
    player = Player.objects.get(user=user)
    earnedBadges = EarnedBadge.objects.filter(player=player)
    return render(request, "registration/settings.html", {'earnedBadges':earnedBadges})

def locations(request):
    """This function renders the locations page"""
    data = Location.objects.all()
    return render(request, "registration/locations.html", {'locations': data})

def badges(request):
    """This function renders the badges page"""
    data = Badge.objects.all()
    name = request.session.get('username')
    return render(request, "registration/badges.html", {'badges': data})
