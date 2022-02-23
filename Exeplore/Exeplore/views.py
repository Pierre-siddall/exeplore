
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate
from .forms import SignUpForm

def register(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            # login needs to happen
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1') #Is this secure??
            user = authenticate(username = username, password = raw_password)
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect('home') # This needs to redirect to the home page
            # add to database
            
        messages.error(request, "Unsuccessful registration. Invalid information.")
    form = SignUpForm()
    return render(request=request, template_name="registration/register.html", context={"register_form": form})


