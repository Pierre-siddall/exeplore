from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate
from .forms import SignUpForm

def register(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registration successful.")
            return home(request) # This needs to redirect to the home page
        else:
             messages.error(request, "Invalid form input")
    form = SignUpForm()
    return render(request=request, template_name="registration/register.html", context={"register_form": form})

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
                return home(request)
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

def settings(request):
    return render(request=request, template_name="registration/settings.html")

def locations(request):
    return render(request=request, template_name="registration/locations.html")

def badges(request):
    return render(request=request, template_name="registration/badges.html")