from django.db import models

# Create your models here.


class Employee(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    # task_set


class Task(models.Model):
    project = models.ForeignKey(    # Many To One Relationship
        "Project", 
        on_delete=models.CASCADE,
        default=1,
        related_name='tasks'
    )

    assign_to = models.ManyToManyField(
        Employee,
        related_name="tasks"
    )    # Many to Many Relationship

    title = models.CharField(max_length=200)
    description = models.TextField()
    due_date = models.DateField()
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



class Task_Detail(models.Model):
    HIGH = 'H'
    MEDIUM = 'M'
    LOW = 'L'
    PRIORITY_OPTIONS = (
        (HIGH, 'High'),
        (MEDIUM, 'Medium'),
        (LOW, 'Low')
    )

    # One to One
    task = models.OneToOneField(
        Task, 
        on_delete=models.CASCADE,
        related_name='details'
    )     # One TO One Relationship

    assigned_to = models.CharField(max_length=100)
    priority = models.CharField(max_length=1, choices=PRIORITY_OPTIONS, default=LOW)



class Project(models.Model):
    name = models.CharField(max_length=100)
    start_date = models.DateField()
    # task_set

