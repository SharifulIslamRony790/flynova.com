import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.test import Client
from django.contrib.auth import get_user_model

User = get_user_model()

def test_all_pages():
    print("\n" + "="*60)
    print("FLYNOVA PAGE VERIFICATION TEST")
    print("="*60)
    
    client = Client()
    
    # Pages that don't require authentication
    public_pages = [
        ('/', 'Homepage'),
        ('/flights/', 'Flights'),
        ('/hotels/', 'Hotels'),
        ('/packages/', 'Packages'),
        ('/accounts/login/', 'Login'),
        ('/accounts/signup/', 'Signup'),
    ]
    
    print("\n[PUBLIC PAGES]")
    all_ok = True
    for url, name in public_pages:
        try:
            response = client.get(url)
            if response.status_code == 200:
                print(f"  ✓ {name}: OK (200)")
            else:
                print(f"  ✗ {name}: Error ({response.status_code})")
                all_ok = False
        except Exception as e:
            print(f"  ✗ {name}: Exception - {e}")
            all_ok = False
    
    # Login for authenticated pages
    email = "test_pages@example.com"
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        user = User.objects.create_user(username='test_pages', email=email, password='Test@123456')
    
    client.login(username=email, password='Test@123456')
    
    # Pages that require authentication
    auth_pages = [
        ('/bookings/my-bookings/', 'My Bookings'),
    ]
    
    print("\n[AUTHENTICATED PAGES]")
    for url, name in auth_pages:
        try:
            response = client.get(url)
            if response.status_code == 200:
                print(f"  ✓ {name}: OK (200)")
            elif response.status_code == 302:
                print(f"  ⚠ {name}: Redirect ({response.url})")
            else:
                print(f"  ✗ {name}: Error ({response.status_code})")
                all_ok = False
        except Exception as e:
            print(f"  ✗ {name}: Exception - {e}")
            all_ok = False
    
    # Check admin
    print("\n[ADMIN PANEL]")
    try:
        response = client.get('/admin/')
        if response.status_code in [200, 302]:
            print(f"  ✓ Admin Panel: Accessible")
        else:
            print(f"  ✗ Admin Panel: Error ({response.status_code})")
    except Exception as e:
        print(f"  ✗ Admin Panel: Exception - {e}")
    
    print("\n" + "="*60)
    if all_ok:
        print("ALL PAGES VERIFIED SUCCESSFULLY!")
    else:
        print("SOME PAGES HAVE ISSUES - CHECK ABOVE")
    print("="*60)

if __name__ == "__main__":
    test_all_pages()
