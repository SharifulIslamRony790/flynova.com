# ==========================================
# HOTELS APP MODELS
# ==========================================
# This file defines the database schema for the hotels system.
# Features included: Hotel (Basic Details) and Room (Pricing and Types).

from django.db import models

# ---------------------------------------------------------
# 1. HOTEL MODEL
# ---------------------------------------------------------
# Represents the core information about a hotel establishment.
class Hotel(models.Model):
    name = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    address = models.TextField()
    description = models.TextField()
    image = models.ImageField(upload_to='hotels/')
    star_rating = models.IntegerField(default=3)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=5000.00)

    def __str__(self):
        return self.name

# ---------------------------------------------------------
# 2. ROOM MODEL
# ---------------------------------------------------------
# Represents specific rooms available within a given hotel.
class Room(models.Model):
    ROOM_TYPES = (
        ('SINGLE', 'Single'),
        ('DOUBLE', 'Double'),
        ('SUITE', 'Suite'),
        ('FAMILY', 'Family'),
        ('DELUXE', 'Deluxe'),
    )
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='rooms')
    room_type = models.CharField(max_length=10, choices=ROOM_TYPES)
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    capacity = models.IntegerField(default=2)
    image = models.ImageField(upload_to='rooms/', blank=True, null=True)

    def __str__(self):
        return f"{self.hotel.name} - {self.get_room_type_display()}"
