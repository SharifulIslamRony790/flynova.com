# ==========================================
# ACCOUNTS APP URL CONFIGURATION
# ==========================================
# This file maps URL patterns to their respective views for user authentication and profiles.
# Features included: Signup, Login, Logout, Profile Management, and Password Change.

from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # ---------------------------------------------------------
    # 1. AUTHENTICATION (Signup, Login, Logout)
    # ---------------------------------------------------------
    path('signup/', views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # ---------------------------------------------------------
    # 2. PROFILE MANAGEMENT
    # ---------------------------------------------------------
    path('profile/', views.profile_view, name='profile'),
    path('profile/edit/', views.edit_profile_view, name='edit_profile'),
    
    # ---------------------------------------------------------
    # 3. PASSWORD MANAGEMENT
    # ---------------------------------------------------------
    path('profile/password/', auth_views.PasswordChangeView.as_view(
        template_name='accounts/change_password.html',
        success_url='/accounts/profile/?password_changed=True'
    ), name='change_password'),
]
