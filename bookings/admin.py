from django.contrib import admin
from .models import Booking

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'content_object', 'booking_date', 'status', 'total_price')
    list_filter = ('status', 'booking_date', 'content_type')
    search_fields = ('user__username', 'user__email')
    readonly_fields = ('booking_date',)
