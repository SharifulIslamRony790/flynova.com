import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from hotels.models import Hotel
from packages.models import Package

# Sample Bangladesh hotel and package images from Unsplash
hotel_images = {
    "Cox's Bazar": "https://images.unsplash.com/photo-1571896349842-33c89424de2d?w=800",
    "Dhaka": "https://images.unsplash.com/photo-1566073771259-6a8506099945?w=800",
    "Sylhet": "https://images.unsplash.com/photo-1542314831-068cd1dbfeeb?w=800",
    "Chittagong": "https://images.unsplash.com/photo-1445019980597-93fa8acb246c?w=800",
}

package_images = {
    "Cox's Bazar": "https://images.unsplash.com/photo-1559827260-dc66d52bef19?w=800",
    "Sundarbans": "https://images.unsplash.com/photo-1564760055775-d63b17a55c44?w=800",
    "Sylhet": "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=800",
    "Bandarban": "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=800",
}

# Update Hotels
print("Updating Hotels with images...")
for hotel in Hotel.objects.all():
    if hotel.city in hotel_images:
        hotel.image = hotel_images[hotel.city]
        hotel.save()
        print(f"Updated {hotel.name} with image")

# Update Packages
print("\nUpdating Packages with images...")
for package in Package.objects.all():
    for dest, img_url in package_images.items():
        if dest.lower() in package.destination.lower():
            package.image = img_url
            package.save()
            print(f"Updated {package.title} with image")
            break

print("\nAll images updated successfully!")
