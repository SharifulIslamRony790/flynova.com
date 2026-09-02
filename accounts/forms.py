# ==========================================
# ACCOUNTS APP FORMS
# ==========================================
# This file handles the form definitions for user registration and profile management.
# Features included: SignUpForm, UserProfileForm.

from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, UserProfile

# ---------------------------------------------------------
# 1. USER SIGNUP FORM
# ---------------------------------------------------------
# Custom registration form extending the default UserCreationForm.
class SignUpForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email')

# ---------------------------------------------------------
# 2. USER PROFILE FORM
# ---------------------------------------------------------
# Form for users to update their profile details (bio, phone, address, etc).
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('profile_picture', 'full_name', 'phone_number', 'address', 'date_of_birth', 'bio')
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'profile_picture': forms.FileInput(attrs={'class': 'form-control'}),
        }
