import os
import django
from django.utils import timezone
from datetime import timedelta, datetime, timezone as dt_timezone

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from flights.models import Flight, Airport, Airline

def create_only_12_flights():
    print("Deleting all existing flights...")
    Flight.objects.all().delete()
    
    print("Creating airports and airlines...")
    # Get or create airports
    airports = {
        'DAC': Airport.objects.get_or_create(code='DAC', defaults={'name': 'Hazrat Shahjalal International Airport', 'city': 'Dhaka', 'country': 'Bangladesh'})[0],
        'CXB': Airport.objects.get_or_create(code='CXB', defaults={'name': "Cox's Bazar Airport", 'city': "Cox's Bazar", 'country': 'Bangladesh'})[0],
        'CGP': Airport.objects.get_or_create(code='CGP', defaults={'name': 'Shah Amanat International Airport', 'city': 'Chittagong', 'country': 'Bangladesh'})[0],
        'JSR': Airport.objects.get_or_create(code='JSR', defaults={'name': 'Jashore Airport', 'city': 'Jashore', 'country': 'Bangladesh'})[0],
        'ZYL': Airport.objects.get_or_create(code='ZYL', defaults={'name': 'Osmani International Airport', 'city': 'Sylhet', 'country': 'Bangladesh'})[0],
        'SPD': Airport.objects.get_or_create(code='SPD', defaults={'name': 'Saidpur Airport', 'city': 'Saidpur', 'country': 'Bangladesh'})[0],
    }
    
    # Get or create airlines
    airlines = {
        'Biman': Airline.objects.get_or_create(name='Biman Bangladesh')[0],
        'US-Bangla': Airline.objects.get_or_create(name='US-Bangla Airlines')[0],
        'Novoair': Airline.objects.get_or_create(name='Novoair')[0],
        'Regent': Airline.objects.get_or_create(name='Regent Airways')[0],
    }
    
    today = timezone.now().date()
    tomorrow = today + timedelta(days=1)
    
    print("Creating exactly 12 flights for tomorrow...")
    
    # 12 Specific Flights (per person price) - ONLY FOR TOMORROW
    flights_data = [
        # Dhaka to Cox's Bazar (3 flights)
        ('Biman', 'BG-141', 'DAC', 'CXB', '08:00', '09:00', 4500),
        ('US-Bangla', 'BS-341', 'DAC', 'CXB', '10:30', '11:30', 4200),
        ('Novoair', 'VQ-501', 'DAC', 'CXB', '14:00', '15:00', 4800),
        
        # Dhaka to Chittagong (2 flights)
        ('Biman', 'BG-061', 'DAC', 'CGP', '09:00', '10:00', 3500),
        ('US-Bangla', 'BS-161', 'DAC', 'CGP', '16:00', '17:00', 3200),
        
        # Dhaka to Sylhet (2 flights)
        ('Novoair', 'VQ-701', 'DAC', 'ZYL', '11:00', '12:00', 3800),
        ('Regent', 'RX-201', 'DAC', 'ZYL', '15:00', '16:00', 4000),
        
        # Dhaka to Jashore (1 flight)
        ('US-Bangla', 'BS-241', 'DAC', 'JSR', '12:00', '13:00', 2800),
        
        # Dhaka to Saidpur (1 flight)
        ('Regent', 'RX-301', 'DAC', 'SPD', '07:30', '09:00', 4200),
        
        # Return Flights (3 flights)
        ('US-Bangla', 'BS-342', 'CXB', 'DAC', '12:00', '13:00', 4200),
        ('Biman', 'BG-062', 'CGP', 'DAC', '11:00', '12:00', 3500),
        ('Novoair', 'VQ-702', 'ZYL', 'DAC', '17:00', '18:00', 3800),
    ]
    
    # Create ONLY 12 flights for tomorrow
    for airline_name, flight_num, origin, dest, dep_time, arr_time, price in flights_data:
        Flight.objects.create(
            airline=airlines[airline_name],
            flight_number=flight_num,
            origin=airports[origin],
            destination=airports[dest],
            departure_time=datetime.combine(tomorrow, datetime.strptime(dep_time, "%H:%M").time()).replace(tzinfo=dt_timezone.utc),
            arrival_time=datetime.combine(tomorrow, datetime.strptime(arr_time, "%H:%M").time()).replace(tzinfo=dt_timezone.utc),
            price=price
        )
    
    total = Flight.objects.count()
    print(f"\n✓ Created exactly {total} flights for {tomorrow.strftime('%Y-%m-%d')}")
    print("\nFlight List:")
    for i, flight in enumerate(Flight.objects.all(), 1):
        print(f"{i}. {flight.flight_number}: {flight.origin.city} → {flight.destination.city} (BDT {flight.price})")

if __name__ == '__main__':
    create_only_12_flights()
