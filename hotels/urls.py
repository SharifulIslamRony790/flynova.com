# ==========================================
# HOTELS APP URL CONFIGURATION
# ==========================================
# This file maps URL patterns for searching and viewing hotels.
# Features included: Hotel Search Page.

from django.urls import path
from . import views

urlpatterns = [
    # ---------------------------------------------------------
    # 1. HOTEL SEARCH
    # ---------------------------------------------------------
    path('', views.search_hotels, name='hotels'),  # Root URL for hotels
    path('search/', views.search_hotels, name='search_hotels'),
]
