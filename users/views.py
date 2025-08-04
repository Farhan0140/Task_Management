from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import Group
from django.contrib.auth.tokens import default_token_generator
from users.forms import CustomRegisterForm, CustomLoginForm, assignRoleForm, CreateGroupForm, CustomPasswordChangeForm, CustomPasswordResetForm, CustomPasswordResetConfirmForm, Edit_Profile_Form
from django.contrib.auth.views import LoginView, PasswordChangeView, PasswordResetView, PasswordResetConfirmView
from django.views.generic import TemplateView, UpdateView, FormView, View, ListView
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

User = get_user_model()

class Sign_Up( FormView ):
    form_class = CustomRegisterForm
    template_name = "registration/register.html"
    success_url = reverse_lazy("sign_in")

    def form_valid(self, form):
        user = form.save(commit = False)
        user.is_active = False
        user.save()
        messages.success(self.request, "A confirmation mail send to your email, Please check your mail box")
        return super().form_valid(form)


class Activate_user(View):
    def get(self, request, user_id, token):
        user = get_object_or_404(User, id=user_id)

        if default_token_generator.check_token(user, token):
            if not user.is_active:
                user.is_active = True
                user.save()
                messages.success(request, "Your account has been activated. Please sign in.")
            else:
                messages.info(request, "Account is already activated. Please sign in.")
            return redirect("sign_in")
        else:
            messages.error(request, "Activation link is invalid or has expired.")
            return redirect("sign_up")



class Sign_In( LoginView ):
    form_class = CustomLoginForm

    def get_success_url(self):
        next_url = self.request.GET.get('next')
        return next_url if next_url else super().get_success_url()
    

def is_admin(user):
    return user.groups.filter(name='Admin').exists()


class Admin_Dashboard(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = User
    template_name = "admin/dashboard.html"
    context_object_name = "users"
    login_url = "sign_in"  
    raise_exception = False 

    def test_func(self):
        return is_admin(self.request.user)

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return super().handle_no_permission()
        return redirect("no_permission")


class Assign_Role(LoginRequiredMixin, UserPassesTestMixin, View):
    login_url = 'sign_in'

    def test_func(self):
        return is_admin(self.request.user)

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return redirect('sign_in')
        return redirect('no_permission')

    def get(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        form = assignRoleForm()
        return render(request, "admin/assign_role.html", {"form": form, "user": user})

    def post(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        form = assignRoleForm(request.POST)
        if form.is_valid():
            role = form.cleaned_data.get('role')
            user.groups.clear()
            user.groups.add(role)
            messages.success(request, f"User '{user.username}' has been assigned to '{role.name}' role.")
            return redirect('admin_dashboard')
        return render(request, "admin/assign_role.html", {"form": form, "user": user})


class Create_Group(LoginRequiredMixin, UserPassesTestMixin, FormView):
    template_name = "admin/create_group.html"
    form_class = CreateGroupForm
    success_url = reverse_lazy("create_group")
    login_url = "sign_in"

    def test_func(self):
        return is_admin(self.request.user)

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return redirect("sign_in")
        return redirect("no_permission")

    def form_valid(self, form):
        group = form.save()
        messages.success(self.request, f"The '{group.name}' group was created successfully.")
        return super().form_valid(form)


class View_Group_List_With_Permission(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Group
    template_name = "admin/group_list.html"
    context_object_name = "groups"
    login_url = "sign_in"

    def test_func(self):
        return is_admin(self.request.user)

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return redirect("sign_in")
        return redirect("no_permission")


class User_Profile( TemplateView ):
    template_name = 'accounts/profile.html'

    def get_context_data(self, **kwargs):

        user = self.request.user

        context = super().get_context_data(**kwargs)
        context["user_name"] = user.username
        context["full_name"] = user.get_full_name()
        context["email"] = user.email
        context["bio"] = user.bio
        context["profile_image"] = user.profile_image

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
 

class Update_Profile( UpdateView ):
    model = User
    form_class = Edit_Profile_Form
    template_name = "accounts/update_profile.html"

    def get_object(self):
        return self.request.user
    
    
    def form_valid(self, form):
        form.save(commit=True)
        return redirect('user_profile')
    