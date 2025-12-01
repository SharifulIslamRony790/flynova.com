from django.contrib import admin
from .models import Hotel, Room

class RoomInline(admin.TabularInline):
    model = Room
    extra = 1

@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'star_rating')
    list_filter = ('city', 'star_rating')
    search_fields = ('name', 'city')
    inlines = [RoomInline]

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('hotel', 'room_type', 'price_per_night', 'capacity')
    list_filter = ('hotel', 'room_type')
