from django import forms
from flights.models import Flight

# ==========================================
# 1. FLIGHT FORM
# ==========================================
# Handles creation and updating of flight schedules in the admin dashboard.
# Includes validation to ensure flight prices are strictly positive.
class FlightForm(forms.ModelForm):
    class Meta:
        model = Flight
        fields = ['airline', 'flight_number', 'origin', 'destination', 'departure_time', 'arrival_time', 'price']
        widgets = {
            'airline': forms.Select(attrs={'class': 'form-select'}),
            'flight_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. BG-123'}),
            'origin': forms.Select(attrs={'class': 'form-select'}),
            'destination': forms.Select(attrs={'class': 'form-select'}),
            'departure_time': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'arrival_time': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0.00'}),
        }

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price is not None and price <= 0:
            raise forms.ValidationError("Price must be greater than zero.")
        return price


# ==========================================
# 2. HOTEL FORM
# ==========================================
# Handles creation and updating of hotels and accommodations.
# Includes zero-trust validation for star ratings (1-5).
from hotels.models import Hotel
class HotelForm(forms.ModelForm):
    class Meta:
        model = Hotel
        fields = ['name', 'city', 'address', 'description', 'price', 'star_rating', 'image']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'star_rating': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 5}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
        }

    def clean_star_rating(self):
        rating = self.cleaned_data.get('star_rating')
        if rating is not None and (rating < 1 or rating > 5):
            raise forms.ValidationError("Star rating must be between 1 and 5.")
        return rating

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price is not None and price <= 0:
            raise forms.ValidationError("Price must be greater than zero.")
        return price


# ==========================================
# 3. HOLIDAY PACKAGE FORM
# ==========================================
# Handles creation and updating of tour/holiday packages.
# Enforces strictly positive pricing for packages.
from packages.models import Package
class PackageForm(forms.ModelForm):
    class Meta:
        model = Package
        fields = ['title', 'destination', 'duration_days', 'duration_nights', 'price', 'overview', 'image']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'destination': forms.TextInput(attrs={'class': 'form-control'}),
            'duration_days': forms.NumberInput(attrs={'class': 'form-control'}),
            'duration_nights': forms.NumberInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'overview': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
        }

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price is not None and price <= 0:
            raise forms.ValidationError("Price must be greater than zero.")
        return price


# ==========================================
# 4. BOOKING STATUS UPDATE FORM
# ==========================================
# A lightweight form used to quickly update a booking's status 
# (e.g., from PENDING to CONFIRMED) without modifying other booking details.
from bookings.models import Booking
class BookingStatusForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['status']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-select'}),
        }
