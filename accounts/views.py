# ==========================================
# ACCOUNTS APP VIEWS
# ==========================================
# This file contains the logic for handling user authentication and profile views.
# Features included: Profile Dashboard, Edit Profile, Signup, and Logout.

from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import SignUpForm, UserProfileForm
from .models import UserProfile
from bookings.models import Booking
from django.db.models import Sum
from django_ratelimit.decorators import ratelimit

# ---------------------------------------------------------
# 1. USER PROFILE VIEW
# ---------------------------------------------------------
# Displays the user's profile information, booking stats, and recent bookings.
@login_required
def profile_view(request):
    try:
        profile = request.user.profile
    except UserProfile.DoesNotExist:
        profile = UserProfile.objects.create(user=request.user)
        
    total_bookings = Booking.objects.filter(user=request.user, status='CONFIRMED').count()
    total_spent = Booking.objects.filter(user=request.user, status='CONFIRMED').aggregate(Sum('total_price'))['total_price__sum'] or 0
    recent_bookings = Booking.objects.filter(user=request.user).order_by('-booking_date')[:3]
    
    context = {
        'profile': profile,
        'total_bookings': total_bookings,
        'total_spent': total_spent,
        'recent_bookings': recent_bookings
    }
    return render(request, 'accounts/profile.html', context)

# ---------------------------------------------------------
# 2. EDIT PROFILE VIEW
# ---------------------------------------------------------
# Allows users to update their personal information and profile picture.
@login_required
def edit_profile_view(request):
    try:
        profile = request.user.profile
    except UserProfile.DoesNotExist:
        profile = UserProfile.objects.create(user=request.user)
        
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'Your profile has been updated successfully!')
                return redirect('profile')
            except Exception as e:
                messages.error(request, 'An error occurred while updating your profile. Please try again.')
    else:
        form = UserProfileForm(instance=profile)
        
    return render(request, 'accounts/edit_profile.html', {'form': form})

# ---------------------------------------------------------
# 3. USER SIGNUP
# ---------------------------------------------------------
# Handles user registration with rate limiting to prevent spam.
@ratelimit(key='ip', rate='5/m', block=True)
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            try:
                user = form.save()
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                messages.success(request, 'Account created successfully!')
                return redirect('home')
            except Exception as e:
                messages.error(request, 'An error occurred during signup. Please try again later.')
    else:
        form = SignUpForm()
    return render(request, 'accounts/signup.html', {'form': form})

# ---------------------------------------------------------
# 4. USER LOGOUT
# ---------------------------------------------------------
# Logs the user out and redirects to the home page.
def logout_view(request):
    logout(request)
    return redirect('home')
