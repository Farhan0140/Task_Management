from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from users.forms import CustomRegisterForm


# Create your views here.


def sign_up(request):

    form = CustomRegisterForm()

    if request.method == "POST":
        form = CustomRegisterForm(request.POST)
        if form.is_valid():
            form.save()

            messages.success(request, "User Created Successfully")
            return redirect("sign_up")


    context = {
        "form": form,
    }

    return render(request, "registration/register.html", context)


def sign_in(request):

    if request.method == "POST":
        userName = request.POST.get("user_name")
        password = request.POST.get("password")

        user = authenticate(request, username = userName, password = password)

        if user is not None:
            login(request, user)
            return redirect("user_dashboard")
        
    return render(request, "registration/login.html")


def sign_out(request):
    if request.method == "POST":
        logout(request)
        return redirect("sign_in")
    
    return redirect("sign_in")
    
