
from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from django.core.mail import send_mail
from tasks.models import Tasks



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

