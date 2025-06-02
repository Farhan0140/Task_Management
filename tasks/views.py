from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def test(request):
    names = ['Farhan', 'Nadim', 'Mr. x', 'Ms. y', 'Baten']
    ages = [12, 23, 45, 56, 67]

    context = {
        "names": names,
        "ages": ages
    }   

    return render(request, "test.html", context)

def manager_dashboard(request):
    return render(request, "dashboard/manager_dashboard.html")


def user_dashboard(request):
    return render(request, "dashboard/User_Dashboard.html")

