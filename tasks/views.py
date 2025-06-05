from django.shortcuts import render
from django.http import HttpResponse
from tasks.forms import Task_Form, Task_Model_Form
from tasks.models import *

# Create your views here.

def test(request):  
    return render(request, "Html Massages/successful.html")

def manager_dashboard(request):
    return render(request, "dashboard/manager_dashboard.html")


def user_dashboard(request):
    return render(request, "dashboard/User_Dashboard.html")

def create_task(request):

    # Django Form

    # employees_from_db = Employee.objects.all()
    # # print(employees_from_db)
    # form = Task_Form(employees = employees_from_db)
    
    # if request.method == 'POST':
    #     form = Task_Form(request.POST, employees = employees_from_db)
    #     # print(form)
    #     if form.is_valid():
    #         # print(form.cleaned_data)
    #         cln_data = form.cleaned_data

    #         title = cln_data.get("title")
    #         description = cln_data.get("description")
    #         due_date = cln_data.get("due_date")
    #         employees_id = cln_data.get("assign_to") 
            
    #         print(title, description, due_date, employees_id)
    #         new_task = Task.objects.create(title=title, description=description, due_date=due_date)

    #         for emp_id in employees_id:
    #             emp = Employee.objects.get(id=emp_id)
    #             new_task.assign_to.add(emp)
            # return render(request, "Task_Form.html", {"form": form, "massage": "Task Added Successfully"})


    # Django Model Form

    form = Task_Model_Form()

    if request.method == 'POST':
        form = Task_Model_Form(request.POST)

        if form.is_valid():
            form.save()

            return render(request, 'Task_Form.html', {'form': form, 'massage': "Task Added Successfully"})


    context = {"form": form}
    return render(request, "Task_Form.html", context)