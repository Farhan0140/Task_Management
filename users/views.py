from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.models import User, Group
from django.contrib.auth.tokens import default_token_generator
from users.forms import CustomRegisterForm, CustomLoginForm, assignRoleForm, CreateGroupForm, CustomPasswordChangeForm, CustomPasswordResetForm, CustomPasswordResetConfirmForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.views import LoginView, PasswordChangeView, PasswordResetView, PasswordResetConfirmView
from django.views.generic import TemplateView
from django.urls import reverse_lazy


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
            return redirect("home")
        
    return render(request, "registration/login.html", {"form": form})


class Sign_In( LoginView ):
    form_class = CustomLoginForm

    def get_success_url(self):
        next_url = self.request.GET.get('next')
        return next_url if next_url else super().get_success_url()



@login_required
def sign_out(request):
    if request.method == "POST":
        logout(request)
        return redirect("sign_in")
    
    return redirect("sign_in")
    

def is_admin(user):
    return user.groups.filter(name='Admin').exists()


@user_passes_test(is_admin, login_url='no_permission')
def admin_dashboard(request):
    users = User.objects.all()

    context = {
        "users" : users,
    }
    return render(request, "admin/dashboard.html", context)


@user_passes_test(is_admin, login_url='no_permission')
def Assign_role(request, user_id):
    user = User.objects.get(id=user_id)
    form = assignRoleForm()

    if request.method == 'POST':
        form = assignRoleForm(request.POST)
        if form.is_valid():
            role = form.cleaned_data.get('role')

            user.groups.clear()
            user.groups.add(role)
            messages.success(request, f"assigned {user.username} has been assign to {role.name} role")
            return redirect('admin_dashboard')
    
    return render(request, "admin/assign_role.html", {"form": form})


@user_passes_test(is_admin, login_url='no_permission')
def create_group(request):
    form = CreateGroupForm()

    if request.method == "POST":
        form = CreateGroupForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f"The {form.cleaned_data.get('name')} was created successfully")
            return redirect('create_group')
    
    return render(request, "admin/create_group.html", {"form": form})


@user_passes_test(is_admin, login_url='no_permission')
def view_group_list_with_permission(request):
    groups = Group.objects.all()

    return render(request, "admin/group_list.html", {"groups": groups})


class User_Profile( TemplateView ):
    template_name = 'accounts/profile.html'

    def get_context_data(self, **kwargs):

        user = self.request.user

        context = super().get_context_data(**kwargs)
        context["user_name"] = user.username
        context["full_name"] = user.get_full_name()
        context["email"] = user.email

        context["date_joined"] = user.date_joined
        context["last_login"] = user.last_login
        return context
    

class Change_Password( PasswordChangeView ):
    form_class = CustomPasswordChangeForm
    template_name = "accounts/change_password.html"


class PasswordReset( PasswordResetView ):
    form_class = CustomPasswordResetForm
    template_name = 'registration/reset_password.html'
    success_url = reverse_lazy('sign_in')
    html_email_template_name = "registration/reset_email.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["protocol"] = "https" if self.request.is_secure() else "http"
        context["domain"] = self.request.get_host()
        return context
    

    def form_valid(self, form):
        messages.success(self.request, "A reset email send, Please check your email")

        return super().form_valid(form)
    

class Confirm_Reset_Password( PasswordResetConfirmView ):
    form_class = CustomPasswordResetConfirmForm
    template_name = 'registration/reset_password.html'
    success_url = reverse_lazy('sign_in')

    def form_valid(self, form):
        messages.success(self.request, "Password Reset Successfully")

        return super().form_valid(form)