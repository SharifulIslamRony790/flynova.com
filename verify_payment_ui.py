import os
import django
import time
from playwright.sync_api import sync_playwright

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model
from flights.models import Flight, Airline, Airport
from bookings.models import Booking
from django.utils import timezone
from datetime import timedelta
from django.contrib.contenttypes.models import ContentType

User = get_user_model()

def verify_ui():
    email = "screenshot_user@example.com"
    password = "password123"
    
    # Ensure user exists (reuse from previous script logic or get)
    try:
        user = User.objects.get(email=email)
        user.set_password(password)
        user.save()
    except User.DoesNotExist:
        user = User.objects.create_user(username="screen_user", email=email, password=password)

    # Ensure booking exists
    # Create valid objects for generic FK
    airline, _ = Airline.objects.get_or_create(name="Nova Test Air")
    dac, _ = Airport.objects.get_or_create(code="DAC")
    cxb, _ = Airport.objects.get_or_create(code="CXB")
    
    flight, _ = Flight.objects.get_or_create(
        flight_number="TEST999", 
        defaults={
            'airline': airline, 'origin': dac, 'destination': cxb,
            'departure_time': timezone.now(), 'arrival_time': timezone.now(),
            'price': 1000
        }
    )

    booking = Booking.objects.create(
        user=user,
        content_type=ContentType.objects.get_for_model(Flight),
        object_id=flight.id,
        total_price=1000,
        status='PENDING'
    )

    base_url = "http://127.0.0.1:8000"
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        # Login
        print("Logging in...")
        page.goto(f"{base_url}/accounts/login/")
        page.fill("input[name='login']", email)
        page.fill("input[name='password']", password)
        page.click("button[type='submit']")
        page.wait_for_url(base_url)
        
        # Go to checkout
        print(f"Navigating to checkout for Booking #{booking.id}")
        page.goto(f"{base_url}/bookings/checkout/{booking.id}/")
        
        # Check for payment method select
        if page.is_visible("select[name='payment_method']"):
            print("SUCCESS: Payment Method selector is visible.")
        else:
            print("FAILURE: Payment Method selector NOT found.")
            print("Dump of form content:")
            element = page.query_selector("#payment-form")
            if element:
                print(element.inner_html())
            else:
                print("Form #payment-form not found.")

        page.screenshot(path="debug_checkout.png")
        print("Screenshot saved to debug_checkout.png")
        
        browser.close()

if __name__ == "__main__":
    verify_ui()
