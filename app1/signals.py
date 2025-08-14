# signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CustomUser

@receiver(post_save, sender=CustomUser)
def profile_picture_updated(sender, instance, **kwargs):
    # Perform actions when the profile picture is updated
    if instance.profile_picture:
        print(f"Profile picture for user {instance.username} has been updated.")
