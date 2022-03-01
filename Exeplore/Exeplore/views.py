from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate
from .forms import SignUpForm, PlayerForm
from django.contrib.auth.models import Group
def register(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        player_form = PlayerForm(request.POST)
        if form.is_valid():
            if player_form.is_valid():
                user =form.save()
                group  = Group.objects.get(name = 'Player')
                user.groups.add(group)
                messages.success(request, "Registration successful.")
                return redirect('/home/') # This needs to redirect to the home page
            else:
                messages.error(request, player_form.errors)
                messages.error(request, "invalid - user")
        else:
            messages.error(request, form.errors)
            messages.error(request, "Invalid form input - original")
    form = SignUpForm()
    player_form = PlayerForm()
    return render(request=request, template_name="registration/register.html", context={"register_form": form, "player_form":form})

def login_view(request):
    if request.method == "POST":
        Authform = AuthenticationForm(request, data=request.POST)
        if Authform.is_valid():
            Uname = Authform.cleaned_data.get('username')
            Pword = Authform.cleaned_data.get('password')
            user = authenticate(username=Uname, password=Pword)
            if user is not None:
                login(request, user)
                messages.info(request, "logged in as", Uname, ".")
                return redirect('/home/')
            else:
                messages.error(request,"Invalid username and/or password")
        else:
            messages.error(request,"Invalid username and/or password")
    Authform = AuthenticationForm()
    return render(request=request, template_name="registration/login.html", context={"login_form": Authform})


def home(request):
    return render(request=request, template_name="registration/home.html")

def splash(request):
    return render(request=request, template_name="registration/splash.html")
