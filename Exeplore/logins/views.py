from django.shortcuts import render, redirect
from .forms import registerForm
from django.contrib import messages

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

