# ==========================================
# ACCOUNTS APP SIGNALS
# ==========================================
# This file handles Django signals for automatic actions triggered by database events.
# Features included: Automatic Profile Creation on User Signup.

from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CustomUser, UserProfile

# ---------------------------------------------------------
# 1. CREATE USER PROFILE
# ---------------------------------------------------------
# Automatically creates a UserProfile instance when a new CustomUser is created.
@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if kwargs.get('raw', False):
        return
    if created:
        UserProfile.objects.create(user=instance)

# ---------------------------------------------------------
# 2. SAVE USER PROFILE
# ---------------------------------------------------------
# Ensures the UserProfile is saved whenever the CustomUser object is saved.
@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    if kwargs.get('raw', False):
        return
    if hasattr(instance, 'profile'):
        instance.profile.save()
    else:
        UserProfile.objects.create(user=instance)
