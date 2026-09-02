# ==========================================
# ACCOUNTS APP ADMIN CONFIGURATION
# ==========================================
# This file registers the custom user model with Django's built-in admin panel.
# Features included: CustomUserAdmin.

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

# ---------------------------------------------------------
# 1. CUSTOM USER ADMIN
# ---------------------------------------------------------
# Customizes how the user model is displayed in the Django Admin portal.
@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['email', 'username', 'is_staff', 'is_active']
    ordering = ['email']
