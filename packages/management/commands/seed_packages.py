import random
from django.core.management.base import BaseCommand
from packages.models import Package, Itinerary

class Command(BaseCommand):
    help = 'Deletes all existing packages and seeds 5 new Holiday Packages.'

    def handle(self, *args, **kwargs):
        self.stdout.write("Deleting existing packages...")
        deleted_count, _ = Package.objects.all().delete()
        self.stdout.write(self.style.SUCCESS(f"Deleted {deleted_count} packages."))

        packages_data = [
            {
                'title': 'Bali Tropical Paradise',
                'destination': 'Bali, Indonesia',
                'duration_days': 5,
                'duration_nights': 4,
                'price': 45000.00,
                'overview': 'Experience the pristine beaches, ancient temples, and vibrant culture of Bali in this 5-day tropical getaway.',
                'image': 'https://images.unsplash.com/photo-1537996194471-e657df975ab4?w=800',
                'itinerary': [
                    'Arrival in Bali, transfer to hotel and evening leisure.',
                    'Full day tour of Ubud, Monkey Forest, and Tegalalang Rice Terrace.',
                    'Visit to Uluwatu Temple and enjoy the Kecak Fire Dance at sunset.',
                    'Water sports at Nusa Dua and visit to Tanah Lot temple.',
                    'Breakfast at hotel, free time for shopping, and departure.'
                ]
            },
            {
                'title': 'Majestic Dubai Experience',
                'destination': 'Dubai, UAE',
                'duration_days': 4,
                'duration_nights': 3,
                'price': 55000.00,
                'overview': 'Discover the luxury, modern architecture, and thrilling desert safaris in the heart of Dubai.',
                'image': 'https://images.unsplash.com/photo-1512453979798-5ea266f8880c?w=800',
                'itinerary': [
                    'Arrival, check-in, and Marina Dhow Cruise Dinner.',
                    'Dubai City Tour including Burj Khalifa At The Top.',
                    'Afternoon Desert Safari with BBQ dinner and Belly Dance.',
                    'Shopping at Dubai Mall and departure.'
                ]
            },
            {
                'title': 'Swiss Alps Adventure',
                'destination': 'Zurich, Switzerland',
                'duration_days': 6,
                'duration_nights': 5,
                'price': 120000.00,
                'overview': 'Enjoy the breathtaking views of the Swiss Alps, serene lakes, and scenic train rides.',
                'image': 'https://images.unsplash.com/photo-1530122037265-a5f1f91d3b99?w=800',
                'itinerary': [
                    'Arrival in Zurich, transfer to Interlaken.',
                    'Excursion to Jungfraujoch - Top of Europe.',
                    'Scenic train ride to Lucerne.',
                    'Mount Titlis tour with Ice Flyer.',
                    'Explore Zurich city and Rhine Falls.',
                    'Departure from Zurich.'
                ]
            },
            {
                'title': 'Romantic Maldives Retreat',
                'destination': 'Male, Maldives',
                'duration_days': 4,
                'duration_nights': 3,
                'price': 85000.00,
                'overview': 'Relax in luxury overwater bungalows and explore the crystal-clear waters of the Maldives.',
                'image': 'https://images.unsplash.com/photo-1514282401047-d79a71a590e8?w=800',
                'itinerary': [
                    'Arrival in Male, speedboat transfer to resort.',
                    'Day at leisure. Enjoy snorkeling and water activities.',
                    'Spa session and romantic private beach dinner.',
                    'Breakfast and speedboat transfer back to airport.'
                ]
            },
            {
                'title': 'Cox\'s Bazar Weekend Getaway',
                'destination': 'Cox\'s Bazar, Bangladesh',
                'duration_days': 3,
                'duration_nights': 2,
                'price': 15000.00,
                'overview': 'Enjoy the world\'s longest natural sea beach with family and friends.',
                'image': 'https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=800',
                'itinerary': [
                    'Arrival, check-in to resort, and enjoy sunset at the beach.',
                    'Drive along Marine Drive, visit Inani Beach and Himchari.',
                    'Morning beach activities, shopping, and departure.'
                ]
            }
        ]

        self.stdout.write("Generating 5 new Holiday Packages...")
        
        for data in packages_data:
            package = Package.objects.create(
                title=data['title'],
                destination=data['destination'],
                duration_days=data['duration_days'],
                duration_nights=data['duration_nights'],
                price=data['price'],
                overview=data['overview'],
            )
            # set image field text directly as URL
            package.image.name = data['image']
            package.save()
            
            # Create itinerary
            for idx, activity in enumerate(data['itinerary']):
                Itinerary.objects.create(
                    package=package,
                    day_number=idx + 1,
                    activity=activity
                )
            self.stdout.write(f"Added Package: {package.title}")

        self.stdout.write(self.style.SUCCESS("Successfully seeded 5 new Holiday Packages!"))
