from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def test(request):
    return render(request, "test.html")

def manager_dashboard(request):
    return render(request, "dashboard/manager_dashboard.html")


def user_dashboard(request):
    return render(request, "dashboard/User_Dashboard.html")

