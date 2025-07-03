from django.shortcuts import render, redirect
from django.http import HttpResponse
from tasks.forms import Task_Model_Form, Task_Detail_Form
from tasks.models import *
from django.db.models import Count, Q
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test, permission_required

# Create your views here.

def no_permission(request):  
    return render(request, "Html Massages/no_permission.html")


def is_manager(user):
    return user.groups.filter(name='Manager').exists()


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
        task_detail_form = Task_Detail_Form(request.POST)

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
