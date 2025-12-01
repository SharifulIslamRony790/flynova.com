import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

# Delete existing superusers
superusers = User.objects.filter(is_superuser=True)
count = superusers.count()
if count > 0:
    print(f"Deleting {count} existing superuser(s)...")
    superusers.delete()
else:
    print("No existing superusers found.")

# Create new superuser
email = 'flynova12@gmail.com'
password = 'flynova1234'
username = 'admin_flynova' # Required field

try:
    User.objects.create_superuser(username=username, email=email, password=password)
    print(f"Successfully created new superuser: {email}")
except Exception as e:
    print(f"Error creating superuser: {e}")
