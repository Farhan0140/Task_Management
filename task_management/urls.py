"""
URL configuration for task_management project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from debug_toolbar.toolbar import debug_toolbar_urls
from tasks.views import *
from core.views import *
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', home, name='home'),
    path("admin/", admin.site.urls),
    path("no_permission/", no_permission, name="no_permission"),
    # path("manager_dashboard/", manager_dashboard, name="manager_dashboard"),
    path("manager_dashboard/", Manager_Dashboard.as_view(), name="manager_dashboard"),
    # path("user_dashboard/", employee_dashboard, name="employee_dashboard"),
    path("user_dashboard/", Employee_Dashboard.as_view(), name="employee_dashboard"),
    # path("create_task/", create_task, name="create_task"),
    path("create_task/", Create_Task.as_view(), name="create_task"),
    # path("task/<int:task_id>/task_detail", task_details, name="task_detail"),
    path("task/<int:task_id>/task_detail", Task_Details.as_view(), name="task_detail"),
    # path("update_task/<int:id>/", update_task, name="update_task"),
    path("update_task/<int:id>/", Update_Task.as_view(), name="update_task"),
    # path("delete_task/<int:id>/", delete_task, name="delete_task"),
    path("delete_task/<int:id>/", Delete_Task.as_view(), name="delete_task"),
    path("dashboard/", dashboard, name="dashboard"),
    path("user/", include("users.urls"))
] + debug_toolbar_urls()


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
