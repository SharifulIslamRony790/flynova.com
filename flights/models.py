# ==========================================
# FLIGHTS APP MODELS
# ==========================================
# This file defines the database schema for the flights system.
# Features included: Airport, Airline, and Flight models.

from django.db import models

# ---------------------------------------------------------
# 1. AIRPORT MODEL
# ---------------------------------------------------------
# Represents global airports with unique 3-letter IATA codes.
class Airport(models.Model):
    code = models.CharField(max_length=3, unique=True)
    name = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name} ({self.code})"

# ---------------------------------------------------------
# 2. AIRLINE MODEL
# ---------------------------------------------------------
# Represents airline companies operating the flights.
class Airline(models.Model):
    name = models.CharField(max_length=100)
    logo = models.ImageField(upload_to='airlines/', blank=True, null=True)

    def __str__(self):
        return self.name

# ---------------------------------------------------------
# 3. FLIGHT MODEL
# ---------------------------------------------------------
# Represents individual scheduled flights connecting airports.
class Flight(models.Model):
    airline = models.ForeignKey(Airline, on_delete=models.CASCADE)
    flight_number = models.CharField(max_length=10)
    origin = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name='departures')
    destination = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name='arrivals')
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return f"{self.airline.name} {self.flight_number}: {self.origin.code} -> {self.destination.code}"
