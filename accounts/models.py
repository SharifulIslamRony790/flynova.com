# ==========================================
# ACCOUNTS APP MODELS
# ==========================================
# This file defines the database schema for the user accounts.
# Features included: CustomUser (Authentication) and UserProfile (Additional Data).

from django.contrib.auth.models import AbstractUser
from django.db import models

# ---------------------------------------------------------
# 1. CUSTOM USER MODEL
# ---------------------------------------------------------
# Overrides default Django User to use email as the primary identifier instead of username.
class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email

# ---------------------------------------------------------
# 2. USER PROFILE MODEL
# ---------------------------------------------------------
# Stores additional user information like phone number, address, and profile picture.
class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile')
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    full_name = models.CharField(max_length=200, blank=True)
    phone_number = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    date_of_birth = models.DateField(blank=True, null=True)
    bio = models.TextField(blank=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"
