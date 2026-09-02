# ==========================================
# CORE APP URL CONFIGURATION
# ==========================================
# This file maps the root URLs for the core functionality of the application.
# Features included: Home Page.

from django.urls import path
from . import views

urlpatterns = [
    # ---------------------------------------------------------
    # 1. MAIN ENTRY POINT
    # ---------------------------------------------------------
    path('', views.home, name='home'),
]
