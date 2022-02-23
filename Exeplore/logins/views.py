
from django.shortcuts import render, redirect
from .forms import registerForm
from django.contrib.auth import login,authenticate
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm


def register(request):
    if request.method == "POST":
        form = registerForm(request.POST)
        if form.is_valid():
            # login needs to happen
            # add to database
            messages.success(request, "Registration successful.")
        messages.error(request, "Unsuccessful registration. Invalid information.")
    form = registerForm()
    return render(request=request, template_name="logins/register.html", context={"register_form": form})

def login(request):
    if request.method=="POST":
        Authform=AuthenticationForm(request,data=request.POST)
        if form.is_valid():
            Uname=form.cleaned_data.get('username')
            Pword=form.cleaned_data.get('password')
            user=authenticate(username=Uname,password=Pword)
            if user is not None:
                login(request,user)
                messages.info(request,"logged in as",Uname,".")
                return redirect("logins:home")
            else:
                messages.error("Invalid username and/or password")
        else:
            messages.error("Invalid username and/or password")
    Authform=AuthenticationForm()
    return render(request=request,template_name="templates/registration/login.html",context={"login_form":Authform})

