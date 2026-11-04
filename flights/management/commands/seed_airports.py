from django.core.management.base import BaseCommand
from flights.models import Airport

class Command(BaseCommand):
    help = 'Seeds popular international and domestic airports.'

    def handle(self, *args, **kwargs):
        airports_data = [
            # Domestic (Bangladesh)
            {'code': 'DAC', 'name': 'Hazrat Shahjalal International Airport', 'city': 'Dhaka', 'country': 'Bangladesh'},
            {'code': 'CGP', 'name': 'Shah Amanat International Airport', 'city': 'Chittagong', 'country': 'Bangladesh'},
            {'code': 'ZYL', 'name': 'Osmani International Airport', 'city': 'Sylhet', 'country': 'Bangladesh'},
            {'code': 'CXB', 'name': 'Cox\'s Bazar Airport', 'city': 'Cox\'s Bazar', 'country': 'Bangladesh'},
            {'code': 'JSR', 'name': 'Jessore Airport', 'city': 'Jessore', 'country': 'Bangladesh'},
            {'code': 'SPD', 'name': 'Saidpur Airport', 'city': 'Saidpur', 'country': 'Bangladesh'},
            
            # International (Popular Destinations)
            {'code': 'DXB', 'name': 'Dubai International Airport', 'city': 'Dubai', 'country': 'United Arab Emirates'},
            {'code': 'SIN', 'name': 'Changi Airport', 'city': 'Singapore', 'country': 'Singapore'},
            {'code': 'BKK', 'name': 'Suvarnabhumi Airport', 'city': 'Bangkok', 'country': 'Thailand'},
            {'code': 'KUL', 'name': 'Kuala Lumpur International Airport', 'city': 'Kuala Lumpur', 'country': 'Malaysia'},
            {'code': 'JFK', 'name': 'John F. Kennedy International Airport', 'city': 'New York', 'country': 'USA'},
            {'code': 'LHR', 'name': 'Heathrow Airport', 'city': 'London', 'country': 'UK'},
            {'code': 'IST', 'name': 'Istanbul Airport', 'city': 'Istanbul', 'country': 'Turkey'},
            {'code': 'JED', 'name': 'King Abdulaziz International Airport', 'city': 'Jeddah', 'country': 'Saudi Arabia'},
            {'code': 'CCU', 'name': 'Netaji Subhash Chandra Bose International Airport', 'city': 'Kolkata', 'country': 'India'},
            {'code': 'DEL', 'name': 'Indira Gandhi International Airport', 'city': 'New Delhi', 'country': 'India'},
        ]

        self.stdout.write("Seeding airports...")
        count = 0
        for data in airports_data:
            # get_or_create to avoid duplicates if some already exist
            obj, created = Airport.objects.get_or_create(
                code=data['code'],
                defaults={
                    'name': data['name'],
                    'city': data['city'],
                    'country': data['country']
                }
            )
            if created:
                count += 1
                self.stdout.write(f"Added: {data['name']} ({data['code']})")

        self.stdout.write(self.style.SUCCESS(f"Successfully seeded {count} new airports!"))
