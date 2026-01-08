import os
import django
import traceback

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.test import Client
from django.contrib.auth import get_user_model
from flights.models import Flight
from bookings.models import Booking

User = get_user_model()

def test_full_booking_flow():
    print("\n" + "="*60)
    print("FLYNOVA COMPLETE END-TO-END TEST")
    print("="*60)
    
    client = Client()
    email = "ronyislam8121@gmail.com"
    
    # 1. SIGNUP
    print("\n[1] TESTING SIGNUP...")
    try:
        user = User.objects.get(email=email)
        user.delete()
        print(f"    Cleaned up existing user")
    except User.DoesNotExist:
        pass
    
    response = client.post('/accounts/signup/', {
        'username': 'ronyislam8121',
        'email': email,
        'password1': 'Test@123456',
        'password2': 'Test@123456',
    })
    
    if response.status_code == 302:
        print(f"    ✓ Signup successful!")
    else:
        print(f"    ✗ Signup failed: Status {response.status_code}")
        return
    
    # 2. LOGIN (already logged in after signup, but let's verify login works separately)
    print("\n[2] TESTING LOGIN...")
    client.logout()
    logged_in = client.login(username=email, password='Test@123456')
    if logged_in:
        print(f"    ✓ Login successful!")
    else:
        print(f"    ✗ Login failed")
        return
    
    # 3. CHECK FLIGHTS PAGE
    print("\n[3] TESTING FLIGHTS PAGE...")
    response = client.get('/flights/')
    if response.status_code == 200:
        print(f"    ✓ Flights page loads correctly")
    else:
        print(f"    ✗ Flights page error: Status {response.status_code}")
    
    # 4. TEST BOOKING
    print("\n[4] TESTING BOOKING FLOW...")
    flight = Flight.objects.first()
    if not flight:
        print("    ✗ No flights in database to book")
        return
    
    print(f"    Booking flight: {flight.airline.name} - {flight.flight_number}")
    
    # Get checkout page
    response = client.get(f'/bookings/create/flight/{flight.id}/')
    if response.status_code == 200:
        print(f"    ✓ Checkout page loads correctly")
    else:
        print(f"    ✗ Checkout page error: Status {response.status_code}")
        return
    
    # Submit booking with payment
    print("\n[5] SUBMITTING PAYMENT...")
    response = client.post(f'/bookings/create/flight/{flight.id}/', {
        'payment_method': 'BKASH',
        'mobile_number': '01712345678',
        'transaction_id': 'TXN123456TEST',
    })
    
    if response.status_code == 302:
        print(f"    ✓ Booking submitted! Redirected to: {response.url}")
        
        # Check if email was sent (check for booking in DB)
        user = User.objects.get(email=email)
        booking = Booking.objects.filter(user=user).order_by('-id').first()
        if booking:
            print(f"    ✓ Booking created: ID #{booking.id}, Status: {booking.status}")
            print(f"\n[6] EMAIL CONFIRMATION...")
            print(f"    Email should be sent to: {email}")
            print(f"    Check your inbox for booking confirmation!")
        else:
            print(f"    ✗ Booking not found in database")
    else:
        print(f"    ✗ Booking failed: Status {response.status_code}")
        if response.status_code == 200:
            # Check for form errors in response
            content = response.content.decode('utf-8')
            if 'alert-danger' in content:
                print("    Form has validation errors")
    
    # 7. TEST MY BOOKINGS PAGE
    print("\n[7] TESTING MY BOOKINGS PAGE...")
    response = client.get('/bookings/my-bookings/')
    if response.status_code == 200:
        print(f"    ✓ My Bookings page loads correctly")
    else:
        print(f"    ✗ My Bookings page error: Status {response.status_code}")
    
    print("\n" + "="*60)
    print("TEST COMPLETE")
    print("="*60)

if __name__ == "__main__":
    test_full_booking_flow()
