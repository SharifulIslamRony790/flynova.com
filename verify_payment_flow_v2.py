import os
import django
import time
from playwright.sync_api import sync_playwright

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model
from flights.models import Flight, Airline, Airport
from django.utils import timezone
from datetime import timedelta

User = get_user_model()

def verify_flow():
    email = "test_payer@example.com"
    password = "password123"
    
    # Ensure user exists
    user, created = User.objects.get_or_create(username="test_payer", email=email)
    if created:
        user.set_password(password)
        user.save()

    # Create Flight
    airline, _ = Airline.objects.get_or_create(name="Nova Test Air")
    dac, _ = Airport.objects.get_or_create(code="DAC")
    cxb, _ = Airport.objects.get_or_create(code="CXB")
    
    flight, _ = Flight.objects.get_or_create(
        flight_number="TEST_PAY_99", 
        defaults={
            'airline': airline, 'origin': dac, 'destination': cxb,
            'departure_time': timezone.now() + timedelta(days=1),
            'arrival_time': timezone.now() + timedelta(days=1, hours=1),
            'price': 1500
        }
    )

    base_url = "http://127.0.0.1:5000"
    target_url = f"{base_url}/bookings/create/flight/{flight.id}/"
    
    print(f"Target URL: {target_url}")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()
        
        # 1. Login
        print("Logging in...")
        page.goto(f"{base_url}/accounts/login/")
        # Try finding login field by label (most robust)
        try:
            page.get_by_label("Email").fill(email)
            print("Filled email using label.")
        except:
             # Fallback to placeholders or generic inputs if label fails
            if page.get_by_placeholder("Email").is_visible():
                page.get_by_placeholder("Email").fill(email)
            elif page.locator("input[type='email']").is_visible():
                page.locator("input[type='email']").fill(email)
            else:
                print("ERROR: Could not find login/email field!")
                print("Page Content Dump:")
                print(page.content())
                page.screenshot(path="debug_login_field_missing.png")
                return
        page.fill("input[name='password']", password)
        page.click("button[type='submit']")
        page.wait_for_url(base_url)
        print("Login successful.")
        
        # 2. Go to Checkout
        print("Navigating to Checkout...")
        page.goto(target_url)
        
        # 3. Select bKash
        print("Selecting bKash...")
        # Find card with text "Pay with bKash"
        bkash_card = page.locator(".payment-card", has_text="Pay with bKash")
        if not bkash_card.is_visible():
            print("ERROR: bKash card not found!")
            page.screenshot(path="debug_payment_fail.png")
            return
        
        bkash_card.click()
        time.sleep(1) # Wait for UI update
        
        # 4. Click Continue
        print("Clicking Continue...")
        btn_continue = page.locator("#btn-continue")
        if not btn_continue.is_enabled():
            print("ERROR: Continue button is disabled!")
            return
        btn_continue.click()
        
        # 5. Fill Details
        print("Filling Payment Details...")
        # Check if details step is visible
        if not page.locator("#step-payment-details").is_visible():
            print("ERROR: Details step not visible!")
            return

        page.fill("#id_mobile_number", "01700000000")
        page.fill("#id_transaction_id", "TRX123456")
        
        # 6. Submit
        print("Submitting Payment...")
        page.click("button[type='submit']")
        
        # 7. Check Success
        print("Waiting for success page...")
        try:
            page.wait_for_url(f"{base_url}/bookings/success/*", timeout=10000)
            print("SUCCESS! Redirected to booking success page.")
            page.screenshot(path="payment_success.png")
        except:
            print("FAILURE: Did not redirect to success page.")
            print(f"Current URL: {page.url}")
            page.screenshot(path="payment_fail.png")

        browser.close()

if __name__ == "__main__":
    verify_flow()
