from django.contrib import admin
from tasks.models import Tasks, Task_Detail, Projects, Employees

# Register your models here.

admin.site.register(Tasks)
admin.site.register(Task_Detail)
admin.site.register(Projects)
admin.site.register(Employees)