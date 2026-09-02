# ==========================================
# HOTELS APP ADMIN CONFIGURATION
# ==========================================
# This file registers the hotel and room models with Django's built-in admin panel.
# Features included: HotelAdmin and RoomAdmin with Inline models.

from django.contrib import admin
from .models import Hotel, Room

# ---------------------------------------------------------
# 1. INLINE ROOM ADMIN
# ---------------------------------------------------------
# Allows rooms to be added directly within the Hotel admin page.
class RoomInline(admin.TabularInline):
    model = Room
    extra = 1

# ---------------------------------------------------------
# 2. HOTEL ADMIN
# ---------------------------------------------------------
# Customizes how hotels are displayed, filtered, and searched.
@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'star_rating')
    list_filter = ('city', 'star_rating')
    search_fields = ('name', 'city')
    inlines = [RoomInline]

# ---------------------------------------------------------
# 3. ROOM ADMIN
# ---------------------------------------------------------
# Customizes how individual rooms are displayed in the Admin portal.
@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('hotel', 'room_type', 'price_per_night', 'capacity')
    list_filter = ('hotel', 'room_type')
