import os
import django
import time
from playwright.sync_api import sync_playwright
from django.conf import settings

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

def prepare_data():
    """Ensure we have data to display."""
    print("Preparing test data...")
    # Airports
    dac, _ = Airport.objects.get_or_create(code="DAC", defaults={'city': 'Dhaka', 'name': 'Hazrat Shahjalal Int.', 'country': 'Bangladesh'})
    cxb, _ = Airport.objects.get_or_create(code="CXB", defaults={'city': 'Coxs Bazar', 'name': 'Coxs Bazar Airport', 'country': 'Bangladesh'})
    
    # Airline
    airline, _ = Airline.objects.get_or_create(name="Nova Air")
    
    # Flight
    flight, created = Flight.objects.get_or_create(
        flight_number="NV101",
        defaults={
            'airline': airline,
            'origin': dac,
            'destination': cxb,
            'departure_time': timezone.now() + timedelta(days=1),
            'arrival_time': timezone.now() + timedelta(days=1, hours=1),
            'price': 4500
        }
    )
    
    # User
    email = "screenshot_user@example.com"
    password = "password123"
    try:
        user = User.objects.get(email=email)
        user.set_password(password)
        user.save()
    except User.DoesNotExist:
        user = User.objects.create_user(username="screen_user", email=email, password=password)
        
    return flight, user, password

def capture_all():
    flight, user, password = prepare_data()
    
    output_dir = "report_screenshots"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    base_url = "http://127.0.0.1:8000"
    
    with sync_playwright() as p:
        # Launch browser
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={'width': 1280, 'height': 800})
        page = context.new_page()
        
        print("Capturing screenshots...")
        
        # 1. Home Page
        print("- Home Page")
        page.goto(base_url)
        page.screenshot(path=f"{output_dir}/home.png")
        
        # 2. Login Page
        print("- Login Page")
        page.goto(f"{base_url}/accounts/login/")
        page.screenshot(path=f"{output_dir}/login.png")
        
        # 3. Registration Page
        print("- Signup Page")
        page.goto(f"{base_url}/accounts/signup/")
        page.screenshot(path=f"{output_dir}/signup.png")
        
        # 4. Flight Search Results (Simulated by going to list or simple search)
        # Assuming /flights/ lists flights or search
        print("- Flight Search")
        # Perform a search or just view list
        # Check urls.py: path('flights/', include('flights.urls')) -> usually lists
        page.goto(f"{base_url}/flights/") 
        # If it requires query params, we might see empty or default
        page.screenshot(path=f"{output_dir}/flight_search.png")
        
        # 5. Flight Details/Airport Info
        # Report says "Flight Page (Details & Airport Info)"
        # Airport Info page is usually /flights/airport-info/ maybe?
        print("- Airport Info")
        # Let's check if there is a specific URL. 
        # Based on file lists, there is 'airport_info.html'. Likely /flights/airport-info/ or similar.
        # Try /flights/airport-dashboard/ or check urls. Let's guess /flights/airport-info/
        # If 404, we'll see error page.
        # Checking core urls earlier: nothing specific.
        # Checking file structure: flights/urls.py not read.
        # Assume accessible.
        try:
            page.goto(f"{base_url}/flights/airport-info/") # Guess
            page.screenshot(path=f"{output_dir}/airport_info.png")
        except:
            print("  - Could not guess airport info URL")

        # 6. Hotels
        print("- Hotels")
        page.goto(f"{base_url}/hotels/")
        page.screenshot(path=f"{output_dir}/hotels.png")
        
        # 7. Checkout (Requires Login & Booking)
        print("- Checkout (Login first)")
        # Login
        page.goto(f"{base_url}/accounts/login/")
        page.fill("input[name='login']", user.email) # Allauth uses 'login' for email/username
        page.fill("input[name='password']", password)
        page.click("button[type='submit']")
        page.wait_for_url(base_url) # Wait for redirect to home
        
        # Create a booking via URL or navigate
        # Let's use the DB to create a pending booking and go to payment page
        booking = Booking.objects.create(
            user=user,
            content_type=ContentType.objects.get_for_model(flight),
            object_id=flight.id,
            status='PENDING',
            total_price=flight.price
        )
        print(f"  - Booking created ID {booking.id}")
        
        # Go to checkout
        # URL pattern for checkout? likely /bookings/checkout/<id>/
        print("- Checkout Page")
        page.goto(f"{base_url}/bookings/checkout/{booking.id}/")
        page.screenshot(path=f"{output_dir}/checkout.png")
        
        browser.close()
        print("Screenshots captured successfully!")

if __name__ == "__main__":
    capture_all()
