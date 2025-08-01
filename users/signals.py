
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User, Group
from django.contrib.auth.tokens import default_token_generator
from django.conf import settings
from django.core.mail import send_mail
from users.models import User_Profile


@receiver(post_save, sender=User)
def send_activation_mail(sender, instance, created, **kwargs):
    if created:
        token = default_token_generator.make_token(instance)
        activation_url = f"{settings.FRONTEND_URL}/user/activate/{instance.id}/{token}/"
        message = f"Hi! {instance.username}\n\nPlease activate your account by clicking the link below\n{activation_url}\n\nThank You"

        try:
            send_mail(
                'Activate Your Account',
                message,
                settings.EMAIL_HOST_USER,
                [instance.email],
                fail_silently=False,
            )
        except Exception as e:
            print(f"Failed to send email to {instance.email}: {str(e)}")


@receiver(post_save, sender=User)
def assign_default_role(sender, instance, created, **kwargs):
    if created:
        user_group, created = Group.objects.get_or_create(name="User")

        instance.groups.add(user_group)
        instance.save()


@receiver( post_save, sender=User )
def after_create(sender, instance, created, **kwargs):
    if created:
        User_Profile.objects.create(user = instance)
