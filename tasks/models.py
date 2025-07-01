from django.db import models
from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from django.core.mail import send_mail


class Employees(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.name


class Tasks(models.Model):

    STATUS_CHOICES = {
        ('PENDING', 'Pending'),
        ('IN_PROGRESS', 'In Progress'),
        ('COMPLETED', 'Completed')
    }

    project = models.ForeignKey(    # Many To One Relationship
        "Projects", 
        on_delete=models.CASCADE,
        default=1,
        related_name='tasks'
    )

    assigned_to = models.ManyToManyField(
        Employees,
        related_name="tasks"
    )    # Many to Many Relationship

    title = models.CharField(max_length=200)
    description = models.TextField()
    due_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title 



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
        Tasks, 
        on_delete=models.CASCADE,
        related_name='details'
    )     # One TO One Relationship

    priority = models.CharField(max_length=1, choices=PRIORITY_OPTIONS, default=LOW)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Details Form Task {self.task.title}"



class Projects(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    start_date = models.DateField()

    def __str__(self):
        return self.name



@receiver(m2m_changed, sender=Tasks.assigned_to.through)
def notify_employees_on_task_creation(sender, instance, action, **kwargs):

    users_mails = [emp.email for emp in instance.assigned_to.all()]

    if action == "post_add":
        send_mail(
            "New task added",
            f"you are assigned to this task {instance.title}",
            "farhannadim2022@gmail.com",
            users_mails,
            fail_silently=False,
        )

