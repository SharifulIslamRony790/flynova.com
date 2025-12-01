import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from flights.models import Flight, Airport

print(f"Total Airports: {Airport.objects.count()}")
print(f"Total Flights: {Flight.objects.count()}")

if Flight.objects.exists():
    f = Flight.objects.first()
    print(f"Sample Flight: {f.flight_number} | {f.origin.code} -> {f.destination.code} | {f.departure_time}")
else:
    print("No flights found in database.")
