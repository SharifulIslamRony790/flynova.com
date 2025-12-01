from django.db import models

class Package(models.Model):
    title = models.CharField(max_length=200)
    destination = models.CharField(max_length=100)
    duration_days = models.IntegerField()
    duration_nights = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    overview = models.TextField()
    image = models.ImageField(upload_to='packages/')

    def __str__(self):
        return self.title

class Itinerary(models.Model):
    package = models.ForeignKey(Package, on_delete=models.CASCADE, related_name='itinerary')
    day_number = models.IntegerField()
    activity = models.TextField()

    class Meta:
        ordering = ['day_number']

    def __str__(self):
        return f"{self.package.title} - Day {self.day_number}"
