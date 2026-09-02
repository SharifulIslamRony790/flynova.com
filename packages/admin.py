# ==========================================
# PACKAGES APP ADMIN CONFIGURATION
# ==========================================
# This file registers the package and itinerary models with Django's built-in admin panel.
# Features included: PackageAdmin and ItineraryInline.

from django.contrib import admin
from django.utils.html import format_html
from .models import Package, Itinerary

# ---------------------------------------------------------
# 1. INLINE ITINERARY ADMIN
# ---------------------------------------------------------
# Allows itinerary days to be added directly within the Package admin page.
class ItineraryInline(admin.TabularInline):
    model = Itinerary
    extra = 1

# ---------------------------------------------------------
# 2. PACKAGE ADMIN
# ---------------------------------------------------------
# Customizes how holiday packages are displayed, filtered, and searched.
@admin.register(Package)
class PackageAdmin(admin.ModelAdmin):
    list_display = ('title', 'destination', 'duration_days', 'price', 'image_tag')
    list_filter = ('destination',)
    search_fields = ('title', 'destination')
    inlines = [ItineraryInline]

    def image_tag(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="60" height="40" style="object-fit: cover;" />', obj.image.url)
        return "-"
    image_tag.short_description = 'Image'
