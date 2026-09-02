# ==========================================
# PACKAGES APP URL CONFIGURATION
# ==========================================
# This file maps URL patterns for searching and viewing holiday packages.
# Features included: Package Search and Package Details.

from django.urls import path
from . import views

urlpatterns = [
    # ---------------------------------------------------------
    # 1. PACKAGE SEARCH & DETAILS
    # ---------------------------------------------------------
    path('', views.search_packages, name='packages'),  # Root URL for packages
    path('search/', views.search_packages, name='search_packages'),
    path('<int:pk>/', views.package_detail, name='package_detail'),
]
