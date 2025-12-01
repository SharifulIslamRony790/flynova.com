import os
import django
from django.utils import timezone
from datetime import timedelta, datetime, timezone as dt_timezone

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

# Get or create airlines
biman = Airline.objects.get_or_create(name='Biman Bangladesh')[0]
usbangla = Airline.objects.get_or_create(name='US-Bangla Airlines')[0]
novoair = Airline.objects.get_or_create(name='Novoair')[0]
regent = Airline.objects.get_or_create(name='Regent Airways')[0]

tomorrow = timezone.now().date() + timedelta(days=1)

print("Creating 12 flights...")

# Flight 1: Dhaka to Cox's Bazar - Biman
Flight.objects.create(
    airline=biman, flight_number='BG-141', origin=dac, destination=cxb,
    departure_time=datetime.combine(tomorrow, datetime.strptime("08:00", "%H:%M").time()).replace(tzinfo=dt_timezone.utc),
    arrival_time=datetime.combine(tomorrow, datetime.strptime("09:00", "%H:%M").time()).replace(tzinfo=dt_timezone.utc),
    price=4500
)

# Flight 2: Dhaka to Cox's Bazar - US-Bangla
Flight.objects.create(
    airline=usbangla, flight_number='BS-341', origin=dac, destination=cxb,
    departure_time=datetime.combine(tomorrow, datetime.strptime("10:30", "%H:%M").time()).replace(tzinfo=dt_timezone.utc),
    arrival_time=datetime.combine(tomorrow, datetime.strptime("11:30", "%H:%M").time()).replace(tzinfo=dt_timezone.utc),
    price=4200
)

# Flight 3: Dhaka to Cox's Bazar - Novoair
Flight.objects.create(
    airline=novoair, flight_number='VQ-501', origin=dac, destination=cxb,
    departure_time=datetime.combine(tomorrow, datetime.strptime("14:00", "%H:%M").time()).replace(tzinfo=dt_timezone.utc),
    arrival_time=datetime.combine(tomorrow, datetime.strptime("15:00", "%H:%M").time()).replace(tzinfo=dt_timezone.utc),
    price=4800
)

# Flight 4: Dhaka to Chittagong - Biman
Flight.objects.create(
    airline=biman, flight_number='BG-061', origin=dac, destination=cgp,
    departure_time=datetime.combine(tomorrow, datetime.strptime("09:00", "%H:%M").time()).replace(tzinfo=dt_timezone.utc),
    arrival_time=datetime.combine(tomorrow, datetime.strptime("10:00", "%H:%M").time()).replace(tzinfo=dt_timezone.utc),
    price=3500
)

# Flight 5: Dhaka to Chittagong - US-Bangla
Flight.objects.create(
    airline=usbangla, flight_number='BS-161', origin=dac, destination=cgp,
    departure_time=datetime.combine(tomorrow, datetime.strptime("16:00", "%H:%M").time()).replace(tzinfo=dt_timezone.utc),
    arrival_time=datetime.combine(tomorrow, datetime.strptime("17:00", "%H:%M").time()).replace(tzinfo=dt_timezone.utc),
    price=3200
)

# Flight 6: Dhaka to Sylhet - Novoair
Flight.objects.create(
    airline=novoair, flight_number='VQ-701', origin=dac, destination=zyl,
    departure_time=datetime.combine(tomorrow, datetime.strptime("11:00", "%H:%M").time()).replace(tzinfo=dt_timezone.utc),
    arrival_time=datetime.combine(tomorrow, datetime.strptime("12:00", "%H:%M").time()).replace(tzinfo=dt_timezone.utc),
    price=3800
)

# Flight 7: Dhaka to Sylhet - Regent
Flight.objects.create(
    airline=regent, flight_number='RX-201', origin=dac, destination=zyl,
    departure_time=datetime.combine(tomorrow, datetime.strptime("15:00", "%H:%M").time()).replace(tzinfo=dt_timezone.utc),
    arrival_time=datetime.combine(tomorrow, datetime.strptime("16:00", "%H:%M").time()).replace(tzinfo=dt_timezone.utc),
    price=4000
)

# Flight 8: Dhaka to Jashore - US-Bangla
Flight.objects.create(
    airline=usbangla, flight_number='BS-241', origin=dac, destination=jsr,
    departure_time=datetime.combine(tomorrow, datetime.strptime("12:00", "%H:%M").time()).replace(tzinfo=dt_timezone.utc),
    arrival_time=datetime.combine(tomorrow, datetime.strptime("13:00", "%H:%M").time()).replace(tzinfo=dt_timezone.utc),
    price=2800
)

# Flight 9: Dhaka to Saidpur - Regent
Flight.objects.create(
    airline=regent, flight_number='RX-301', origin=dac, destination=spd,
    departure_time=datetime.combine(tomorrow, datetime.strptime("07:30", "%H:%M").time()).replace(tzinfo=dt_timezone.utc),
    arrival_time=datetime.combine(tomorrow, datetime.strptime("09:00", "%H:%M").time()).replace(tzinfo=dt_timezone.utc),
    price=4200
)

# Flight 10: Cox's Bazar to Dhaka - US-Bangla
Flight.objects.create(
    airline=usbangla, flight_number='BS-342', origin=cxb, destination=dac,
    departure_time=datetime.combine(tomorrow, datetime.strptime("12:00", "%H:%M").time()).replace(tzinfo=dt_timezone.utc),
    arrival_time=datetime.combine(tomorrow, datetime.strptime("13:00", "%H:%M").time()).replace(tzinfo=dt_timezone.utc),
    price=4200
)

# Flight 11: Chittagong to Dhaka - Biman
Flight.objects.create(
    airline=biman, flight_number='BG-062', origin=cgp, destination=dac,
    departure_time=datetime.combine(tomorrow, datetime.strptime("11:00", "%H:%M").time()).replace(tzinfo=dt_timezone.utc),
    arrival_time=datetime.combine(tomorrow, datetime.strptime("12:00", "%H:%M").time()).replace(tzinfo=dt_timezone.utc),
    price=3500
)

# Flight 12: Sylhet to Dhaka - Novoair
Flight.objects.create(
    airline=novoair, flight_number='VQ-702', origin=zyl, destination=dac,
    departure_time=datetime.combine(tomorrow, datetime.strptime("17:00", "%H:%M").time()).replace(tzinfo=dt_timezone.utc),
    arrival_time=datetime.combine(tomorrow, datetime.strptime("18:00", "%H:%M").time()).replace(tzinfo=dt_timezone.utc),
    price=3800
)

print(f"Created {Flight.objects.count()} flights for {tomorrow}")
print("\nFlight List:")
for i, f in enumerate(Flight.objects.all(), 1):
    print(f"{i}. {f.flight_number}: {f.origin.city} -> {f.destination.city} (BDT {f.price})")
