import os
import django
from django.utils import timezone
from datetime import timedelta
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from flights.models import Flight, Airport, Airline

# Get or create airports
dac = Airport.objects.get_or_create(code='DAC', defaults={'name': 'Hazrat Shahjalal International Airport', 'city': 'Dhaka', 'country': 'Bangladesh'})[0]
cxb = Airport.objects.get_or_create(code='CXB', defaults={'name': "Cox's Bazar Airport", 'city': "Cox's Bazar", 'country': 'Bangladesh'})[0]
cgp = Airport.objects.get_or_create(code='CGP', defaults={'name': 'Shah Amanat International Airport', 'city': 'Chittagong', 'country': 'Bangladesh'})[0]
jsr = Airport.objects.get_or_create(code='JSR', defaults={'name': 'Jashore Airport', 'city': 'Jashore', 'country': 'Bangladesh'})[0]
zyl = Airport.objects.get_or_create(code='ZYL', defaults={'name': 'Osmani International Airport', 'city': 'Sylhet', 'country': 'Bangladesh'})[0]
spd = Airport.objects.get_or_create(code='SPD', defaults={'name': 'Saidpur Airport', 'city': 'Saidpur', 'country': 'Bangladesh'})[0]

airports = [dac, cxb, cgp, jsr, zyl, spd]

# Get or create airlines
biman = Airline.objects.get_or_create(name='Biman Bangladesh')[0]
usbangla = Airline.objects.get_or_create(name='US-Bangla Airlines')[0]
novoair = Airline.objects.get_or_create(name='Novoair')[0]
regent = Airline.objects.get_or_create(name='Regent Airways')[0]

airlines = [biman, usbangla, novoair, regent]

print("Creating flights arriving in the next 24 hours...")

now = timezone.now()

count = 0
# Create flights arriving soon (for airport info page)
for i in range(20):
    origin = random.choice(airports)
    destination = random.choice([a for a in airports if a != origin])
    airline = random.choice(airlines)
    
    # Arrivals in next 24 hours
    hours_ahead = random.randint(0, 23)
    minutes_ahead = random.randint(0, 59)
    arrival_time = now + timedelta(hours=hours_ahead, minutes=minutes_ahead)
    departure_time = arrival_time - timedelta(minutes=random.randint(45, 90))
    
    flight_num = f"{airline.name[:2].upper()}-{random.randint(100, 999)}"
    
    Flight.objects.create(
        airline=airline, flight_number=flight_num, origin=origin, destination=destination,
        departure_time=departure_time, arrival_time=arrival_time, price=random.randint(3000, 8000)
    )
    count += 1

print(f"{count} flights created!")
