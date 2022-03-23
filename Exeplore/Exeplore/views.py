"""This file houses the views for the app, including the User registration,
login, and rendering of other pages"""
from datetime import datetime, timezone, timedelta
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate, get_user_model, logout
from django.contrib.auth.models import Group
from django.db.models import Count
from visits.models import Badge, Location
from users.models import Player, EarnedBadge, Visit
from .forms import SignUpForm, PlayerForm, AddLocationForm, AddBadgeForm

User = get_user_model()


def register(request):
    """This method registers a user by using the SignUpForm, and associates a
    Player with them"""
    if request.method == "POST":
        form = SignUpForm(request.POST)
        player_form = PlayerForm(request.POST)
        # if the error is with the user's entries
        if form.is_valid():
            # if there's some error with creating the Player to go with the User
            if player_form.is_valid():
                user = form.save()
                # add the new user to the admin group Player
                group = Group.objects.get(name='Player')
                user.groups.add(group)
                messages.success(request, "Registration successful.")
                request.session['username'] = user.username
                return redirect('/home/')  # redirects to the home page
            else:
                messages.error(request, player_form.errors)
                messages.error(request, "invalid - user")
        else:
            messages.error(request, form.errors)
            messages.error(request, "Invalid form input - original")
    form = SignUpForm()
    player_form = PlayerForm()
    return render(request=request, template_name="registration/register.html",
                  context={"register_form": form, "player_form": form})


def login_view(request):
    """This method defines the login functionality, using the Authentication Form"""
    if request.method == "POST":
        auth_form = AuthenticationForm(request, data=request.POST)
        if auth_form.is_valid():
            username = auth_form.cleaned_data.get('username')
            password = auth_form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                last_login = user.last_login
                login(request, user)
                messages.info(request, "logged in as", username, ".")
                request.session['username'] = username
                if abs(last_login - datetime.now(timezone.utc)) >= timedelta(hours=24):
                    if abs(last_login - datetime.now(timezone.utc)) <= timedelta(hours=48):
                        player = Player.objects.get(user=user)
                        player.extend_streak()
                elif abs(last_login - datetime.now(timezone.utc)) > timedelta(hours=48):
                    player = Player.objects.get(user=user)
                    player.reset_streak()
                return redirect('/home/')
            else:
                messages.error(request, "Invalid username and/or password")
        else:
            messages.error(request, "Invalid username and/or password")
    auth_form = AuthenticationForm()
    return render(request=request, template_name="registration/login.html",
                  context={"login_form": auth_form})


def logout_view(request):
    """This function logs the player out and returns them to the splash screen"""
    logout(request)
    # if some cookies need to be saved even after logout
    # save them here
    return redirect('/splash/')


def home(request):
    """This function renders the home page - this also writes locations to a file"""
    name = request.session.get('username')
    user = User.objects.get(username=name)
    data = Location.objects.all()

    location_names = []
    lats = []
    lngs = []
    for location in data:
        lats.append(float(location.get_lat()))
        lngs.append(float(location.get_long()))
        location_names.append(location.get_name())
    return render(request, "registration/home.html", {'user': user, 'lats': lats, 'lngs': lngs, 'lct_name': location_names})


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
        developer = False
        if not permission:
            developer = user.groups.filter(name='Developer').exists()
        if developer:
            permission = True
        earned_badges = EarnedBadge.objects.filter(player=player)
        visits = Visit.objects.filter(player=player)
        return render(request, "registration/settings.html", {'user': user,
                                                              'earnedBadges': earned_badges, 'visits': visits, 'permission': permission,
                                                              'developer': developer})
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
        found = False
        for a in all_locations:
            if a.location_name == v.location.location_name:
                found = True
                break
        if not found:
            all_locations.append(v.location)
    for item in data:
        if item in all_locations:
            data.remove(item)
    return render(request, "registration/locations.html", {'locations': data, 'visits': all_locations})


def badges(request):
    """This function renders the badges page"""
    data = Badge.objects.all()
    data = list(data)
    name = request.session.get('username')
    user = User.objects.get(username=name)
    player = Player.objects.get(user=user)
    earned_badges = EarnedBadge.objects.filter(player=player)
    all_badges = []
    for earned_badge in earned_badges:
        all_badges.append(earned_badge.badge)
    for item in data:
        if item in all_badges:
            data.remove(item)
    return render(request, "registration/badges.html", {'badges': data, 'earnedBadges': all_badges})


def add_location(request):
    """This view is for gamekeepers and developers to add locations"""
    if request.method == "POST":
        form = AddLocationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()  # add a location
            messages.success(request, "Location adding successful.")
            return redirect('/settings/')  # redirects to the settings page
        else:  # if the error is with the user's entries
            messages.error(request, form.errors)
            messages.error(request, "invalid - location")
            print(form.errors)
    form = AddLocationForm()
    return render(request=request, template_name="registration/add_location.html",
                  context={"location_form": form})


def del_location(request):
    """This view is to delete locations from the database for gamekeepers
    and developers"""
    if request.method == "POST":
        # remove the correct location
        Location.objects.filter(id=request.POST["location"]).delete()
        messages.success(request, "Location deleting successful.")
        return redirect('/settings/')  # redirects to the settings page
    data = Location.objects.all()
    return render(request=request, template_name="registration/del_location.html",
                  context={"locations": data})


def add_badge(request):
    """This view is for gamekeepers and developers to add a new badge to
    the database"""
    if request.method == "POST":
        form = AddBadgeForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()  # save the new badge
            messages.success(request, "Badge adding successful.")
            return redirect('/settings/')  # redirects to the settings page
        else:  # if the error is with the user's entries
            messages.error(request, form.errors)
            messages.error(request, "invalid - badge")
            print(form.errors)
    form = AddBadgeForm()
    return render(request=request, template_name="registration/add_badge.html",
                  context={"badge_form": form})


def del_badge(request):
    """This view is for a gamekeeper or developer to delete a badge
    from the database"""
    if request.method == "POST":
        # remove the correct badge
        Badge.objects.filter(id=request.POST["badge"]).delete()
        messages.success(request, "Badge deleting successful.")
        return redirect('/settings/')  # redirects to the settings page
    data = Badge.objects.all()
    return render(request=request, template_name="registration/del_badge.html",
                  context={"badges": data})


def add_user(request):
    """This view is for a developer to add a new user"""
    if request.method == "POST":
        # use the existing sign up form for efficiency
        form = SignUpForm(request.POST)
        # get the selected group
        group = request.POST["group"]
        if form.is_valid():
            user = form.save()  # save the new user
            # add the new user to the given group
            group = Group.objects.get(name=group)
            user.groups.add(group)
            messages.success(request, "User adding successful.")
            return redirect('/settings/')  # redirects to the settings page
        else:  # if the error is with the user's entries
            messages.error(request, form.errors)
            messages.error(request, "invalid - user")
            print(form.errors)
    form = SignUpForm()
    return render(request=request, template_name="registration/add_user.html",
                  context={"user_form": form})


def del_user(request):
    """This view allows for a developer to delete a user"""
    if request.method == "POST":
        # remove the correct user
        User.objects.filter(id=request.POST["user"]).delete()
        messages.success(request, "User deleting successful.")
        return redirect('/settings/')  # redirects to the settings page
    data = User.objects.all()
    return render(request=request, template_name="registration/del_user.html",
                  context={"users": data})


def edit_user(request):
    """This view is so a developer can edit a user"""
    if request.method == "POST":
        # find the user, group, and action
        user = User.objects.get(id=request.POST["user"])
        group = Group.objects.get(name=request.POST["group"])
        action = request.POST["action"]
        if action == 'add':
            # add user to the new group
            user.groups.add(group)
        else:
            # remove the user from the group
            user.groups.remove(group)
        messages.success(request, "User editing successful.")
        return redirect('/settings/')  # redirects to the settings page
    users = User.objects.all()
    return render(request=request, template_name="registration/edit_user.html",
                  context={"users": users})


def check_badges(user):
    """This is the function to check if any of the badges' requirements
    have been fulfilled, and adds it to the database"""
    list_of_badges = Badge.objects.all()
    player = Player.objects.get(user=user)
    list_of_visits = Visit.objects.filter(player=player)
    for earned_badge in list_of_badges:
        if not EarnedBadge.objects.filter(player=player, badge=earned_badge).exists():
            if earned_badge.badge_name == "Navigator":
                for visit in list_of_visits:
                    if visit.__str__() == "Truro Campus":
                        achievement = EarnedBadge(
                            player=player, badge=earned_badge, badge_earned_datetime=datetime.now())
                        achievement.save()
            elif earned_badge.badge_name == "Apprentice Astronaut":
                if list_of_visits.count() >= 25:
                    achievement = EarnedBadge(
                        player=player, badge=earned_badge, badge_earned_datetime=datetime.now())
                    achievement.save()
            elif earned_badge.badge_name == "Novice Astronaut":
                if list_of_visits.count() >= 10:
                    achievement = EarnedBadge(
                        player=player, badge=earned_badge, badge_earned_datetime=datetime.now())
                    achievement.save()
            elif earned_badge.badge_name == "Scanmaster":
                list_of_player = Player.objects.all()
                scanmaster = player
                for p_in_list in list_of_player:
                    if Visit.objects.filter(player=p_in_list).count() >= list_of_visits.count():
                        scanmaster = p_in_list
                if scanmaster == player:
                    achievement = EarnedBadge(
                        player=player, badge=earned_badge, badge_earned_datetime=datetime.now())
                    achievement.save()
            elif earned_badge.badge_name == "Supernova":
                if player.streak >= 365:
                    achievement = EarnedBadge(
                        player=player, badge=earned_badge, badge_earned_datetime=datetime.now())
                    achievement.save()
            elif earned_badge.badge_name == "Blue Supergiant Star":
                if player.streak >= 30:
                    achievement = EarnedBadge(
                        player=player, badge=earned_badge, badge_earned_datetime=datetime.now())
                    achievement.save()
            elif earned_badge.badge_name == "Red Giant Star":
                if player.streak >= 7:
                    achievement = EarnedBadge(
                        player=player, badge=earned_badge, badge_earned_datetime=datetime.now())
                    achievement.save()
            elif earned_badge.badge_name == "Participation Award":
                if list_of_visits.count() > 0:
                    achievement = EarnedBadge(
                        player=player, badge=earned_badge, badge_earned_datetime=datetime.now())
                    achievement.save()
            # elif b.badge_name == "Deadline Daredevil":
            elif earned_badge.badge_name == "Creature of Habit":
                most_common = Visit.objects.filter(player=player).values(
                    'location').annotate(num_occur=Count('location')).order_by('-num_occur')
                #top_location = most_common[0]['location']
                top_location_count = Visit.objects.filter(
                    location=most_common[0]['location']).count()
                if top_location_count/list_of_visits.count() >= 0.75:
                    achievement = EarnedBadge(
                        player=player, badge=earned_badge, badge_earned_datetime=datetime.now())
                    achievement.save()
            elif earned_badge.badge_name == "Jack of All Planets":
                important_building_counter = 0
                for visit in list_of_visits:
                    if visit.__str__() == "XFi Building":
                        important_building_counter += 1
                    if visit.__str__() == "Streatham Court":
                        important_building_counter += 1
                    if visit.__str__() == "Physics Building":
                        important_building_counter += 1
                    if visit.__str__() == "Harrison Building":
                        important_building_counter += 1
                    if visit.__str__() == "Forum":
                        important_building_counter += 1
                    if visit.__str__() == "Amory Building":
                        important_building_counter += 1
                if important_building_counter == 6:
                    achievement = EarnedBadge(
                        player=player, badge=earned_badge, badge_earned_datetime=datetime.now())
                    achievement.save()
            elif earned_badge.badge_name == "Top of the World":
                for visit in list_of_visits:
                    if visit.__str__() == "Physics Building":
                        achievement = EarnedBadge(
                            player=player, badge=earned_badge, badge_earned_datetime=datetime.now())
                        achievement.save()
            elif earned_badge.badge_name == "Galactic Hipster":
                for visit in list_of_visits:
                    if visit.__str__() == "Costa Coffee":
                        achievement = EarnedBadge(
                            player=player, badge=earned_badge, badge_earned_datetime=datetime.now())
                        achievement.save()
            # elif b.badge_name == "Sputnik":
            elif earned_badge.badge_name == "Master Astronaut":
                if list_of_visits.count() >= 100:
                    achievement = EarnedBadge(
                        player=player, badge=earned_badge, badge_earned_datetime=datetime.now())
                    achievement.save()
            elif earned_badge.badge_name == "Adept Astronaut":
                if list_of_visits.count() >= 50:
                    achievement = EarnedBadge(
                        player=player, badge=earned_badge, badge_earned_datetime=datetime.now())
                    achievement.save()


def scanning(request):
    """This view renders and processes the scanning of QR codes"""
    if request.method == "POST":
        # saving the fact the user visited a location
        location = Location.objects.get(location_name=request.POST["location"])
        name = request.session.get('username')
        user = User.objects.get(username=name)
        player = Player.objects.get(user=user)
        current_datetime = datetime.now()
        # make the visit
        visit = Visit.objects.create(
            player=player, location=location, visit_datetime=current_datetime)
        # save the player's new score
        player.set_score(location)
        player.save()
        visit.save()
        check_badges(user)
        messages.success(request, "Visit logging successful.")
        if (request.POST["answer"] == request.POST["radio"]):
            messages.success(request, "Correct answer! Well done!")
            #double points from the location when the question is correct:
            player.set_score(location)
            player.save()
        else:
            messages.success(
                request, "Incorrect answer! Better luck next time!")
        return redirect('/locations/')  # redirects to the locations page
    return render(request=request, template_name="registration/scanning.html")


def leaderboard(request):
    # list of players ordered by score
    player = Player.objects.all().order_by('-score')
    return render(request=request, template_name="registration/leaderboard.html", context={"player": player})
