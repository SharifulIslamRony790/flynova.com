# ==========================================
# FLIGHTS APP URL CONFIGURATION
# ==========================================
# This file maps URL patterns for flight browsing and information.
# Features included: Flight Search and Real-time Airport Info.

from django.urls import path
from . import views

urlpatterns = [
    # ---------------------------------------------------------
    # 1. FLIGHT SEARCH
    # ---------------------------------------------------------
    path('', views.search_flights, name='flights'),  # Root URL for flights
    path('search/', views.search_flights, name='search_flights'),
    
    # ---------------------------------------------------------
    # 2. AIRPORT INFORMATION
    # ---------------------------------------------------------
    path('airport-info/', views.airport_info, name='airport_info'),
]
