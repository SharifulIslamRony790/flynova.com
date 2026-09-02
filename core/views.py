# ==========================================
# CORE APP VIEWS
# ==========================================
# This file contains the logic for the core pages of the application.
# Features included: Home Page.

from django.shortcuts import render
from flights.models import Airport

# ---------------------------------------------------------
# 1. HOME PAGE
# ---------------------------------------------------------
# Renders the main landing page and provides airport data for the search bar.
def home(request):
    airports = Airport.objects.all().order_by('city')
    return render(request, 'core/home.html', {'airports': airports})
