from django.test import Client
from django.contrib.auth import get_user_model
from bookings.models import Booking
from flights.models import Flight, Airline, Airport
from django.utils import timezone
from datetime import timedelta
import io

User = get_user_model()

def run_test():
    print("\n[START] COMPREHENSIVE SYSTEM TEST")
    
    client = Client()
    email = "test_full@example.com"
    username = "test_full_user"
    password = "password123"

    # --- CLEANUP ---
    try:
        u = User.objects.get(email=email)
        u.delete()
        print("[INFO] Cleaned up existing test user.")
    except User.DoesNotExist:
        pass

    # --- 1. SIGN UP ---
    print("\n[1] Testing Sign Up...")
    try:
        user = User.objects.create_user(username=username, email=email, password=password)
        print(f"[OK] User created: {user.email}")
    except Exception as e:
        print(f"[FAIL] Sign up failed: {e}")
        return

    # --- 2. LOGIN ---
    print("\n[2] Testing Login...")
    logged_in = client.login(email=email, password=password)
    # Note: If backend uses username, client.login might need username. 
    # Let's try both or check USERNAME_FIELD.
    if not logged_in:
        logged_in = client.login(username=username, password=password)
    
    if logged_in:
        print("[OK] Login successful")
    else:
        print("[FAIL] Login failed")
        return

    # --- 3. CREATE BOOKING ---
    print("\n[3] Testing Booking Creation...")
    # Need a flight first
    try:
        airport1, _ = Airport.objects.get_or_create(code="DAC", defaults={'city': 'Dhaka', 'name': 'Hazrat Shahjalal International Airport', 'country': 'Bangladesh'})
        airport2, _ = Airport.objects.get_or_create(code="CXB", defaults={'city': 'Coxs Bazar', 'name': 'Coxs Bazar Airport', 'country': 'Bangladesh'})
        airline, _ = Airline.objects.get_or_create(name="Test Airline")
        
        flight = Flight.objects.create(
            airline=airline,
            flight_number="TEST101",
            origin=airport1,
            destination=airport2,
            departure_time=timezone.now() + timedelta(days=1),
            arrival_time=timezone.now() + timedelta(days=1, hours=1),
            price=5000
        )
        
        # Create booking via view or model? 
        # Let's create via model to save time, as we want to test PDF download mostly.
        from django.contrib.contenttypes.models import ContentType
        booking = Booking.objects.create(
            user=user,
            content_type=ContentType.objects.get_for_model(Flight),
            object_id=flight.id,
            total_price=5000,
            status='CONFIRMED'
        )
        print(f"[OK] Booking created: ID #{booking.id}")
    except Exception as e:
        print(f"[FAIL] Booking creation failed: {e}")
        return

    # --- 4. TEST PDF DOWNLOAD ---
    print("\n[4] Testing PDF Download...")
    try:
        response = client.get(f'/bookings/download-pdf/{booking.id}/')
        if response.status_code == 200:
            if response['Content-Type'] == 'application/pdf':
                print(f"[OK] PDF Download successful. Size: {len(response.content)} bytes")
            else:
                print(f"[FAIL] PDF Download returned wrong content type: {response['Content-Type']}")
        else:
            print(f"[FAIL] PDF Download failed with status code: {response.status_code}")
            print(f"Response content: {response.content}")
    except Exception as e:
        print(f"[FAIL] PDF Download exception: {e}")

    # --- 5. TEST USER DELETION & RE-SIGNUP ---
    print("\n[5] Testing User Deletion & Re-signup...")
    try:
        user.delete()
        print(f"[OK] User deleted: {email}")
        
        # Re-create
        user = User.objects.create_user(username=username, email=email, password=password)
        print(f"[OK] User RE-CREATED successfully with same email: {user.email}")
    except Exception as e:
        print(f"[FAIL] User deletion/re-creation failed: {e}")

    print("\n[END] TEST COMPLETE")

if __name__ == "__main__":
    run_test()
