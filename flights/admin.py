# ==========================================
# FLIGHTS APP ADMIN CONFIGURATION
# ==========================================
# This file registers the flight models with Django's built-in admin panel.
# Features included: AirportAdmin, AirlineAdmin, and FlightAdmin.

from django.contrib import admin
from .models import Airport, Airline, Flight

# ---------------------------------------------------------
# 1. AIRPORT ADMIN
# ---------------------------------------------------------
# Customizes how airports are displayed and searched in the Admin portal.
@admin.register(Airport)
class AirportAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'city', 'country')
    search_fields = ('code', 'name', 'city')

# ---------------------------------------------------------
# 2. AIRLINE ADMIN
# ---------------------------------------------------------
# Customizes how airlines are displayed in the Admin portal.
@admin.register(Airline)
class AirlineAdmin(admin.ModelAdmin):
    list_display = ('name',)

# ---------------------------------------------------------
# 3. FLIGHT ADMIN
# ---------------------------------------------------------
# Customizes how flights are displayed, filtered, and searched.
@admin.register(Flight)
class FlightAdmin(admin.ModelAdmin):
    list_display = ('flight_number', 'airline', 'origin', 'destination', 'departure_time', 'price')
    list_filter = ('airline', 'origin', 'destination', 'departure_time')
    search_fields = ('flight_number', 'origin__code', 'destination__code')
    date_hierarchy = 'departure_time'
