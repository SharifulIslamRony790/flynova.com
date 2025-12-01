from django.contrib import admin
from .models import Airport, Airline, Flight

@admin.register(Airport)
class AirportAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'city', 'country')
    search_fields = ('code', 'name', 'city')

@admin.register(Airline)
class AirlineAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Flight)
class FlightAdmin(admin.ModelAdmin):
    list_display = ('flight_number', 'airline', 'origin', 'destination', 'departure_time', 'price')
    list_filter = ('airline', 'origin', 'destination', 'departure_time')
    search_fields = ('flight_number', 'origin__code', 'destination__code')
    date_hierarchy = 'departure_time'
