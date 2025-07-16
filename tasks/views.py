from django.shortcuts import render, redirect
from django.http import HttpResponse
from tasks.forms import Task_Model_Form, Task_Detail_Form
from tasks.models import *
from django.db.models import Count, Q
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test, permission_required
from users.views import is_admin
from django.views.generic import ListView, DetailView, UpdateView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin, PermissionRequiredMixin

# Create your views here.

def no_permission(request):  
    return render(request, "Html Massages/no_permission.html")


def is_manager(user):
    return (user.groups.filter(name='Manager').exists()) or (user.groups.filter(name='Admin').exists())


def is_employee(user):
    return user.groups.filter(name='Employee').exists()


@login_required(redirect_field_name='sign_in')
@user_passes_test(is_manager, login_url='no_permission')
def manager_dashboard(request):

    type = request.GET.get('type', 'all')

    base_query = Tasks.objects.select_related('details').prefetch_related('assigned_to')
    if type == "completed":
        tasks = base_query.filter(status='COMPLETED')
    elif type == "in_progress":
        tasks = base_query.filter(status='IN_PROGRESS')
    elif type == "pending":
        tasks = base_query.filter(status='PENDING')
    else:
        tasks = base_query.all()

    counts = Tasks.objects.aggregate(
        total_task=Count('id'),
        completed_task=Count('id', filter=Q(status = "COMPLETED")),
        task_in_progress=Count('id', filter=Q(status = "IN_PROGRESS")),
        pending = Count('id', filter=Q(status = "PENDING"))
    )

    context = {
        "tasks": tasks,
        "counts": counts
    }

    return render(request, "dashboard/manager_dashboard.html", context)


@login_required(redirect_field_name='sign_in')
@user_passes_test(is_employee, login_url='no_permission')
def employee_dashboard(request):
    return render(request, "dashboard/User_Dashboard.html")



@login_required(redirect_field_name='sign_in')
@permission_required("tasks.add_tasks", login_url='no_permission')
def create_task(request):
    task_form = Task_Model_Form()
    task_detail_form = Task_Detail_Form()


    if request.method == 'POST':
        task_form = Task_Model_Form(request.POST)
        task_detail_form = Task_Detail_Form(request.POST, request.FILES)

        if task_form.is_valid() and task_detail_form.is_valid():
            task = task_form.save()
            task_detail = task_detail_form.save(commit=False)
            task_detail.task = task
            task_detail.save()

            messages.success(request, "Task Added Successfully")
            return redirect("create_task")


    context = {'task':task_form, 'task_detail': task_detail_form}
    return render(request, "Task_Form.html", context)



@login_required(redirect_field_name='sign_in')
@permission_required("tasks.change_tasks", login_url='no_permission')
def update_task(request, id):

    task = Tasks.objects.get(id = id)
    task_form = Task_Model_Form(instance=task)
    task_detail_form = Task_Detail_Form(instance=task.details)


    if request.method == 'POST':
        task_form = Task_Model_Form(request.POST, instance=task)
        task_detail_form = Task_Detail_Form(request.POST, instance=task.details)

        if task_form.is_valid() and task_detail_form.is_valid():
            task = task_form.save()
            task_detail = task_detail_form.save(commit=False)
            task_detail.task = task
            task_detail.save()

            messages.success(request, "Task Update Successfully")
            return redirect("update_task", id)


    context = {'task':task_form, 'task_detail': task_detail_form}
    return render(request, "Task_Form.html", context)



@login_required(redirect_field_name='sign_in')
@permission_required("tasks.delete_tasks", login_url='no_permission')
def delete_task(request, id):
    task = Tasks.objects.get(id=id)

    if request.method == 'POST':
        task.delete()

        messages.success(request, "Task Deleted Successfully")
        return redirect("manager_dashboard")



@login_required(redirect_field_name='sign_in')
@permission_required("tasks.view_task_detail", login_url='no_permission')
def task_details(request, task_id):
    task_detail = Tasks.objects.get(id = task_id)
    status_choices = Tasks.STATUS_CHOICES

    if request.method == "POST":
        selected_status = request.POST.get('Task_Status')
        task_detail.status = selected_status
        task_detail.save()
        return redirect('task_detail', task_detail.id)

    return render(request, "task_details.html", {"task": task_detail, "status_choices": status_choices})


def dashboard(request):
    user = request.user
    if is_admin(user):
        return redirect("admin_dashboard")
    elif is_manager(user):
        return redirect("manager_dashboard")
    elif is_employee(user):
        return redirect("employee_dashboard")
    
    return redirect("no_permission")



# _______________ Class View _________________


class Manager_Dashboard(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Tasks
    template_name = "dashboard/manager_dashboard.html"
    context_object_name = 'tasks'
    
    login_url = "sign_in"

    def test_func(self):
        return is_manager(self.request.user)
    
    def handle_no_permission(self):
        return redirect('no_permission')

    def get_queryset(self):
        type = self.request.GET.get('type', all)
        base_query = Tasks.objects.select_related('details').prefetch_related('assigned_to')

        if type == "completed":
            tasks = base_query.filter(status='COMPLETED')
        elif type == "in_progress":
            tasks = base_query.filter(status='IN_PROGRESS')
        elif type == "pending":
            tasks = base_query.filter(status='PENDING')
        else:
            tasks = base_query.all()

        return tasks
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["counts"] = counts = Tasks.objects.aggregate(
                                total_task=Count('id'),
                                completed_task=Count('id', filter=Q(status = "COMPLETED")),
                                task_in_progress=Count('id', filter=Q(status = "IN_PROGRESS")),
                                pending = Count('id', filter=Q(status = "PENDING"))
                            )
        return context
    



class Create_Task(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    template_name = 'Task_form.html'
    context_object_name = 'task'
    form_class = Task_Model_Form

    login_url = 'sign_in'
    permission_required = 'tasks.add_tasks'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['task'] = context['form']
        if 'task_detail' not in context:
            context["task_detail"] = Task_Detail_Form()
        return context
    
    def post(self, request, *args, **kwargs):
        self.object = None
        task_form = self.get_form()
        detail_form = Task_Detail_Form(request.POST, request.FILES)

        if task_form.is_valid() and detail_form.is_valid():
            detail = detail_form.save(commit=False)
            task = task_form.save()
            detail.task = task
            detail.save()
            messages.success(request, "Task Added Successfully")

            return redirect("create_task")



class Task_Details(DetailView):
    model = Tasks
    template_name = "task_details.html"
    context_object_name = 'task'
    pk_url_kwarg = 'task_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["status_choices"] = Tasks.STATUS_CHOICES
        return context
    
    def post(self, request, *args, **kwargs):
        task_detail = self.get_object()
        selected_status = request.POST.get('Task_Status')
        task_detail.status = selected_status
        task_detail.save()
        return redirect('task_detail', task_detail.id)
    
    

class Update_Task(UpdateView):
    model = Tasks
    form_class = Task_Model_Form
    template_name = "Task_Form.html"
    context_object_name = 'task'
    pk_url_kwarg = 'id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["task"] = self.get_form()

        if hasattr(self.object, 'details') and self.object.details:
            context['task_detail'] = Task_Detail_Form(instance = self.object.details)
        else:
            context['task_detail'] = Task_Detail_Form()
        # context['task_detail'] = Task_Detail_Form(instance = self.object.details)
        return context
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        task_form = Task_Model_Form(request.POST, instance=self.object)
        task_detail_form = Task_Detail_Form(request.POST, request.FILES, instance=getattr(self.object, 'details', None))
        # print(self.object)
        if task_form.is_valid() and task_detail_form.is_valid():
            task = task_form.save()
            task_detail = task_detail_form.save(commit=False)
            task_detail.task = task
            task_detail.save()

            messages.success(request, "Task Update Successfully")
            return redirect("update_task", self.object.id)
        
        else:
            return redirect('update_task', self.object.id)