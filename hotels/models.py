from django.db import models

class Hotel(models.Model):
    name = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    address = models.TextField()
    description = models.TextField()
    image = models.ImageField(upload_to='hotels/')
    star_rating = models.IntegerField(default=3)

    def __str__(self):
        return self.name

class Room(models.Model):
    ROOM_TYPES = (
        ('SINGLE', 'Single'),
        ('DOUBLE', 'Double'),
        ('SUITE', 'Suite'),
    )
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='rooms')
    room_type = models.CharField(max_length=10, choices=ROOM_TYPES)
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    capacity = models.IntegerField(default=2)
    image = models.ImageField(upload_to='rooms/', blank=True, null=True)

    def __str__(self):
        return f"{self.hotel.name} - {self.get_room_type_display()}"
