import os
import django
from django.conf import settings
from django.core.mail import send_mail

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

def test_email():
    print(f"Testing email configuration...")
    print(f"EMAIL_BACKEND: {settings.EMAIL_BACKEND}")
    print(f"EMAIL_HOST: {settings.EMAIL_HOST}")
    print(f"EMAIL_PORT: {settings.EMAIL_PORT}")
    print(f"EMAIL_USE_TLS: {settings.EMAIL_USE_TLS}")
    print(f"EMAIL_HOST_USER: {settings.EMAIL_HOST_USER}")
    # Do not print password
    
    recipient = settings.EMAIL_HOST_USER # Send to self
    
    try:
        print(f"\nAttempting to send test email to {recipient}...")
        send_mail(
            'FlyNova Debug Email',
            'This is a test email from the FlyNova debug script.',
            settings.EMAIL_HOST_USER,
            [recipient],
            fail_silently=False,
        )
        print("SUCCESS: Email sent successfully!")
    except Exception as e:
        print(f"ERROR: Failed to send email.")
        print(f"Error details: {str(e)}")

if __name__ == "__main__":
    test_email()
