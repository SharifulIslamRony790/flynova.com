# ==========================================
# MAIN PROJECT URL CONFIGURATION (FLYNOVA)
# ==========================================
# This file acts as the central router for the entire Django project.
# It delegates URL handling to the respective application's urls.py files.

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # ---------------------------------------------------------
    # 1. ADMIN & DASHBOARD
    # ---------------------------------------------------------
    path('flynova-admin/', admin.site.urls), # Secured admin login portal
    path('dashboard/', include('dashboard.urls')), # Custom admin dashboard

    # ---------------------------------------------------------
    # 2. CORE & AUTHENTICATION
    # ---------------------------------------------------------
    path('', include('core.urls')), # Home page
    path('accounts/', include('accounts.urls')), # Custom user auth
    path('accounts/', include('allauth.urls')),  # Google OAuth (Allauth)

    # ---------------------------------------------------------
    # 3. SERVICES (Flights, Hotels, Packages, Bookings)
    # ---------------------------------------------------------
    path('flights/', include('flights.urls')),
    path('hotels/', include('hotels.urls')),
    path('packages/', include('packages.urls')),
    path('bookings/', include('bookings.urls')),
] 

# Serve static/media files during development
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
