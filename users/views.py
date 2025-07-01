from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from users.forms import CustomRegisterForm, CustomLoginForm
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator


# Create your views here.


def sign_up(request):

    form = CustomRegisterForm()

    if request.method == "POST":
        form = CustomRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            messages.success(request, "A confirmation mail send to your email, Please check your mail box")
            return redirect("sign_in")


    context = {
        "form": form,
    }

    return render(request, "registration/register.html", context)


def activate_user(request, user_id, token):
    user = User.objects.get(id=user_id)

    try:
        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return redirect("sign_in")
        else:
            print("This account already activate, login")
    except Exception as e:
        print("user id not found")
    


def sign_in(request):

    form = CustomLoginForm()

    if request.method == "POST":
        form = CustomLoginForm(data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("user_dashboard")
        
    return render(request, "registration/login.html", {"form": form})


def sign_out(request):
    if request.method == "POST":
        logout(request)
        return redirect("sign_in")
    
    return redirect("sign_in")
    

def admin_dashboard(request):
    users = User.objects.all()

    context = {
        "users" : users,
    }
    return render(request, "admin/dashboard.html", context)

