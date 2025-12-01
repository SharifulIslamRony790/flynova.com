from django.db import models

class Airport(models.Model):
    code = models.CharField(max_length=3, unique=True)
    name = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name} ({self.code})"

class Airline(models.Model):
    name = models.CharField(max_length=100)
    logo = models.ImageField(upload_to='airlines/', blank=True, null=True)

    def __str__(self):
        return self.name

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
