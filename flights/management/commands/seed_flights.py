import random
from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from flights.models import Flight, Airport, Airline

class Command(BaseCommand):
    help = 'Deletes all existing flights and seeds 20 new flights with future dates.'

    def handle(self, *args, **kwargs):
        # 1. Delete existing flights
        self.stdout.write("Deleting existing flights...")
        deleted_count, _ = Flight.objects.all().delete()
        self.stdout.write(self.style.SUCCESS(f"Deleted {deleted_count} flights."))

        # 2. Get available Airlines and Airports
        airlines = list(Airline.objects.all())
        airports = list(Airport.objects.all())
        
        if len(airlines) == 0 or len(airports) < 2:
            self.stdout.write(self.style.ERROR("Not enough Airlines or Airports in the database to generate flights."))
            return
            
        # 3. Create 20 new flights
        self.stdout.write("Generating 20 new flights...")
        now = timezone.now()
        
        flights_to_create = []
        for i in range(20):
            airline = random.choice(airlines)
            
            # Pick distinct origin and destination
            origin, destination = random.sample(airports, 2)
            
            # Generate future departure time (between 0 and 30 days from now)
            # Using 0 ensures some flights arrive within the next 24 hours
            days_ahead = random.randint(0, 30)
            hours_ahead = random.randint(0, 23)
            minutes_ahead = random.choice([0, 15, 30, 45])
            
            departure_time = now + timedelta(days=days_ahead, hours=hours_ahead, minutes=minutes_ahead)
            
            # Flight duration between 45 mins and 3 hours
            duration_minutes = random.randint(45, 180)
            arrival_time = departure_time + timedelta(minutes=duration_minutes)
            
            # Random price between 3000 and 12000 BDT
            price = random.randint(30, 120) * 100
            
            # Flight number
            prefix = airline.name[:2].upper()
            flight_number = f"{prefix}-{random.randint(100, 999)}"
            
            flights_to_create.append(
                Flight(
                    airline=airline,
                    flight_number=flight_number,
                    origin=origin,
                    destination=destination,
                    departure_time=departure_time,
                    arrival_time=arrival_time,
                    price=price
                )
            )
            
        Flight.objects.bulk_create(flights_to_create)
        self.stdout.write(self.style.SUCCESS("Successfully seeded 20 new flights!"))
