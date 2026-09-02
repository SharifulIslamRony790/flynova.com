# ==========================================
# BOOKINGS APP ADMIN CONFIGURATION
# ==========================================
# This file registers the booking models with Django's built-in admin panel.
# Features included: BookingAdmin.

from django.contrib import admin
from .models import Booking

# ---------------------------------------------------------
# 1. BOOKING ADMIN
# ---------------------------------------------------------
# Customizes how the bookings are displayed, filtered, and searched in the Admin portal.
@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'get_service', 'booking_date', 'status', 'total_price')
    list_filter = ('status', 'booking_date')
    search_fields = ('user__username', 'user__email')
    readonly_fields = ('booking_date',)
