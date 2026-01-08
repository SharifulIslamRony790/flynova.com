from django.db import models
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

class Booking(models.Model):
    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('CONFIRMED', 'Confirmed'),
        ('CANCELLED', 'Cancelled'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='bookings')
    
    # Generic Relation to link Flight, Room, or Package
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    booking_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Booking #{self.id} - {self.user.email} ({self.status})"

class Payment(models.Model):
    PAYMENT_METHOD_CHOICES = (
        ('BKASH', 'bKash'),
        ('NAGAD', 'Nagad'),
        ('VISA', 'Visa'),
        ('MASTERCARD', 'MasterCard'),
    )

    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name='payment')
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_id = models.CharField(max_length=100, blank=True, null=True, help_text="For Mobile Banking")
    card_last4 = models.CharField(max_length=4, blank=True, null=True, help_text="For Cards")
    timestamp = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='SUCCESS') # SUCCESS or FAILED
    
    def __str__(self):
        return f"Payment #{self.id} for Booking #{self.booking.id}"
