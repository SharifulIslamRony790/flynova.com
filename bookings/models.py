# ==========================================
# BOOKINGS APP MODELS
# ==========================================
# This file defines the database schema for bookings and payments.
# Features included: Booking (Flights, Rooms, Packages) and Payment Tracking.

from django.db import models
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

# ---------------------------------------------------------
# 1. BOOKING MODEL
# ---------------------------------------------------------
# Handles reservations for flights, hotels, or holiday packages by a user.
class Booking(models.Model):
    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('CONFIRMED', 'Confirmed'),
        ('CANCELLED', 'Cancelled'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='bookings')
    
    # Specific Relations (New Architecture)
    flight = models.ForeignKey('flights.Flight', on_delete=models.CASCADE, null=True, blank=True, related_name='bookings')
    room = models.ForeignKey('hotels.Room', on_delete=models.CASCADE, null=True, blank=True, related_name='bookings')
    package = models.ForeignKey('packages.Package', on_delete=models.CASCADE, null=True, blank=True, related_name='bookings')

    booking_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    @property
    def get_service(self):
        return self.flight or self.room or self.package

    def __str__(self):
        return f"Booking #{self.id} - {self.user.email} ({self.status})"

# ---------------------------------------------------------
# 2. PAYMENT MODEL
# ---------------------------------------------------------
# Tracks the transaction status and payment gateway details for a booking.
class Payment(models.Model):
    PAYMENT_METHOD_CHOICES = (
        ('SSLCOMMERZ', 'SSLCommerz (bKash, Cards, NetBanking)'),
        ('BKASH', 'bKash (Manual)'),
        ('NAGAD', 'Nagad (Manual)'),
        ('VISA', 'Visa (Manual)'),
        ('MASTERCARD', 'MasterCard (Manual)'),
    )

    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name='payment')
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, default='SSLCOMMERZ')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_id = models.CharField(max_length=100, blank=True, null=True, help_text="Gateway Transaction ID (tran_id)")
    val_id = models.CharField(max_length=100, blank=True, null=True, help_text="SSLCommerz Validation ID")
    bank_tran_id = models.CharField(max_length=100, blank=True, null=True, help_text="Bank Transaction ID")
    card_last4 = models.CharField(max_length=4, blank=True, null=True, help_text="For Cards")
    timestamp = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='PENDING') # PENDING, SUCCESS, FAILED, CANCELLED
    
    def __str__(self):
        return f"Payment #{self.id} for Booking #{self.booking.id} ({self.status})"
