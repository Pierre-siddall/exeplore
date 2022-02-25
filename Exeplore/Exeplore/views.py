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
            return redirect("logins:index") # This needs to redirect to the home page
        else:
             messages.error(request, "Invalid form input")
    form = SignUpForm()
    return render(request=request, template_name="registration/register.html", context={"register_form": form})

def login(request):
    if request.method == "POST":
        Authform = AuthenticationForm(request, data=request.POST)
        if Authform.is_valid():
            Uname = Authform.cleaned_data.get('username')
            Pword = Authform.cleaned_data.get('password')
            user = authenticate(username=Uname, password=Pword)
            if user is not None:
                login(request, user)
                messages.info(request, "logged in as", Uname, ".")
                return redirect("logins:home")
            else:
                messages.error("Invalid username and/or password")
        else:
            messages.error("Invalid username and/or password")
    Authform = AuthenticationForm()
    return render(request=request, template_name="templates/registration/login.html", context={"login_form": Authform})


