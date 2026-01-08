import os
import django
import traceback

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.test import Client
from django.contrib.auth import get_user_model

User = get_user_model()

def test_signup():
    print("\n[TEST] Testing Signup Flow...")
    
    client = Client()
    
    # First, get the signup page to get CSRF token
    response = client.get('/accounts/signup/')
    print(f"GET /accounts/signup/ - Status: {response.status_code}")
    
    # Clean up any existing test user
    email = "ronyislam8121@gmail.com"
    try:
        user = User.objects.get(email=email)
        user.delete()
        print(f"[INFO] Cleaned up existing user: {email}")
    except User.DoesNotExist:
        pass
    
    # Try to signup
    try:
        response = client.post('/accounts/signup/', {
            'username': 'ronyislam8121',
            'email': email,
            'password1': 'Test@123456',
            'password2': 'Test@123456',
        })
        print(f"POST /accounts/signup/ - Status: {response.status_code}")
        
        if response.status_code == 302:
            print(f"[SUCCESS] Signup successful! Redirected to: {response.url}")
        elif response.status_code == 200:
            # Check for form errors
            if hasattr(response, 'context') and response.context and 'form' in response.context:
                form = response.context['form']
                if form.errors:
                    print(f"[ERROR] Form errors: {form.errors}")
            else:
                print("[INFO] Page rendered but no redirect - check for errors in HTML")
        else:
            print(f"[ERROR] Unexpected status code")
            print(f"Response content: {response.content[:500]}")
            
    except Exception as e:
        print(f"[ERROR] Exception during signup:")
        traceback.print_exc()

if __name__ == "__main__":
    test_signup()
