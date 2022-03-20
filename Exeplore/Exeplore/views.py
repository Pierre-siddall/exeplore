"""This file houses the views for the app, including the User registration,
login, and rendering of other pages"""
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate, get_user_model, logout
from django.contrib.auth.models import Group
from users.models import Player, EarnedBadge, Visit
from visits.models import Location

from visits.models import Badge, Location

from .forms import SignUpForm, PlayerForm, AddLocationForm, AddBadgeForm
User = get_user_model()

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
                user = form.save()
                #add the new user to the admin group Player
                group = Group.objects.get(name = 'Player')
                user.groups.add(group)
                messages.success(request, "Registration successful.")
                request.session['username'] = user.username
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

def logout_view(request):
    logout(request)
    # if some cookies need to be saved even after logout
    # save them here
    return redirect('/splash/')

def home(request):
    """This function renders the home page - this also writes locations to a file"""
    name = request.session.get('username')
    user = User.objects.get(username=name)
    data = Location.objects.all()
    new_file = open("locations.txt", "w")
    
    
    for d in data:
        new_file.write(str(d) + ' ')
        new_file.write(str(d.get_lat()) + ' ')
        new_file.write(str(d.get_long()) + '\n')

    new_file.close()

    """
   
    with ("locations.txt", 'w') as f:
        for d in data:
            f.write(d)
    """

    return render(request, "registration/home.html", {'user':user})

def splash(request):
    """This function renders the splash page"""
    return render(request=request, template_name="registration/splash.html")

def settings(request):
    """This function renders the settings page"""
    try:
        name = request.session.get('username')
        user = User.objects.get(username=name)
        player = Player.objects.get(user=user)
        permission = user.groups.filter(name='Gamekeeper').exists()
        earnedBadges = EarnedBadge.objects.filter(player=player)
        visits = Visit.objects.filter(player=player)
        return render(request, "registration/settings.html", {'user':user, 'earnedBadges':earnedBadges, 'visits':visits, 'permission':permission})
    except:
        return render(request, "registration/splash.html")

def locations(request):
    """This function renders the locations page"""
    data = Location.objects.all()
    data = list(data)
    name = request.session.get('username')
    user = User.objects.get(username=name)
    player = Player.objects.get(user=user)
    visits = Visit.objects.filter(player=player)
    all_locations = []
    for v in visits:
        all_locations.append(v.location)
    for item in data:
        if item in all_locations:
            data.remove(item)
    return render(request, "registration/locations.html", {'locations': data, 'visits':all_locations})

def badges(request):
    """This function renders the badges page"""
    data = Badge.objects.all()
    data = list(data)
    name = request.session.get('username')
    user = User.objects.get(username=name)
    player = Player.objects.get(user=user)
    earned_badges = EarnedBadge.objects.filter(player=player)
    all_badges = []
    for b in earned_badges:
        all_badges.append(b.badge)
    for item in data:
        if item in all_badges:
            data.remove(item)
    return render(request, "registration/badges.html", {'badges': data, 'earnedBadges':all_badges})

def add_location(request):
    if request.method == "POST":
        form = AddLocationForm(request.POST, request.FILES)
        #if the error is with the user's entries
        if form.is_valid():
            form.save()
            messages.success(request, "Location adding successful.")
            return redirect('/settings/') # redirects to the settings page
        else:
            messages.error(request, form.errors)
            messages.error(request, "invalid - location")
            print(form.errors)
    form = AddLocationForm()
    return render(request=request, template_name="registration/add_location.html",
    context={"location_form": form})

def del_location(request):
    if request.method == "POST":
        Location.objects.filter(id=request.POST["location"]).delete()
        messages.success(request, "Location deleting successful.")
        return redirect('/settings/') # redirects to the settings page
    data = Location.objects.all()
    return render(request=request, template_name="registration/del_location.html",
    context={"locations": data})

def add_badge(request):
    if request.method == "POST":
        form = AddBadgeForm(request.POST, request.FILES)
        #if the error is with the user's entries
        if form.is_valid():
            form.save()
            messages.success(request, "Badge adding successful.")
            return redirect('/settings/') # redirects to the settings page
        else:
            messages.error(request, form.errors)
            messages.error(request, "invalid - badge")
            print(form.errors)
    form = AddBadgeForm()
    return render(request=request, template_name="registration/add_badge.html",
    context={"badge_form": form})

def del_badge(request):
    if request.method == "POST":
        Badge.objects.filter(id=request.POST["badge"]).delete()
        messages.success(request, "Badge deleting successful.")
        return redirect('/settings/') # redirects to the settings page
    data = Badge.objects.all()
    return render(request=request, template_name="registration/del_badge.html",
    context={"badges": data})