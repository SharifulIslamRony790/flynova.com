import random
from django.core.management.base import BaseCommand
from hotels.models import Hotel, Room

class Command(BaseCommand):
    help = 'Deletes all existing hotels and seeds 7 new premium Hotels with rooms.'

    def handle(self, *args, **kwargs):
        self.stdout.write("Deleting existing hotels...")
        deleted_count, _ = Hotel.objects.all().delete()
        self.stdout.write(self.style.SUCCESS(f"Deleted {deleted_count} hotels."))

        hotels_data = [
            {
                'name': 'Radisson Blu Water Garden',
                'city': 'Dhaka',
                'address': 'Airport Road, Dhaka Cantonment, Dhaka',
                'description': 'A luxurious 5-star hotel featuring outdoor pools, a spa, and multiple dining options surrounded by lush gardens.',
                'image': 'https://images.unsplash.com/photo-1566073771259-6a8506099945?w=800',
                'star_rating': 5,
                'price': 15000.00
            },
            {
                'name': 'The Peninsula Chittagong',
                'city': 'Chittagong',
                'address': 'Bulbul Center, 486/B O.R. Nizam Road, GEC Circle, Chittagong',
                'description': 'Premium hospitality in the heart of Chittagong with a rooftop pool, international cuisine, and excellent city views.',
                'image': 'https://images.unsplash.com/photo-1582719478250-c89cae4dc85b?w=800',
                'star_rating': 4,
                'price': 8500.00
            },
            {
                'name': 'Sayeman Beach Resort',
                'city': 'Cox\'s Bazar',
                'address': 'Marine Drive Road, Kolatoli, Cox\'s Bazar',
                'description': 'Oceanfront luxury resort offering breathtaking views of the Bay of Bengal and an infinity pool.',
                'image': 'https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?w=800',
                'star_rating': 5,
                'price': 12000.00
            },
            {
                'name': 'Grand Sylhet Hotel & Resort',
                'city': 'Sylhet',
                'address': 'Boroshala, Airport Road, Sylhet',
                'description': 'Experience the beauty of Sylhet in this grand resort surrounded by tea gardens and scenic landscapes.',
                'image': 'https://images.unsplash.com/photo-1455587734955-081b22074882?w=800',
                'star_rating': 5,
                'price': 10500.00
            },
            {
                'name': 'Long Beach Hotel',
                'city': 'Cox\'s Bazar',
                'address': '14 Kalatoli Road, Hotel Motel Zone, Cox\'s Bazar',
                'description': 'A renowned luxury hotel steps away from the beach, featuring excellent amenities and spacious rooms.',
                'image': 'https://images.unsplash.com/photo-1582719508461-905c673771fd?w=800',
                'star_rating': 4,
                'price': 7000.00
            },
            {
                'name': 'InterContinental Dhaka',
                'city': 'Dhaka',
                'address': '1 Minto Road, Dhaka',
                'description': 'The most prestigious luxury hotel in Dhaka, carrying a legacy of excellent hospitality.',
                'image': 'https://images.unsplash.com/photo-1571003123894-1f0594d2b5d9?w=800',
                'star_rating': 5,
                'price': 18000.00
            },
            {
                'name': 'Momo Inn Resort',
                'city': 'Bogra',
                'address': 'Nawdapara, Bogra',
                'description': 'A magnificent 5-star resort in Northern Bangladesh offering premium stay with a large water park and helicopter pad.',
                'image': 'https://images.unsplash.com/photo-1564501049412-61c2a3083791?w=800',
                'star_rating': 5,
                'price': 9500.00
            }
        ]

        self.stdout.write("Generating 7 new Hotels...")
        
        for data in hotels_data:
            hotel = Hotel.objects.create(
                name=data['name'],
                city=data['city'],
                address=data['address'],
                description=data['description'],
                star_rating=data['star_rating'],
                price=data['price']
            )
            # set image field text directly as URL
            hotel.image.name = data['image']
            hotel.save()
            
            # Create a few rooms for this hotel
            room_types = ['SINGLE', 'DOUBLE', 'SUITE', 'DELUXE']
            for r_type in room_types:
                base_price = float(data['price'])
                multiplier = 1.0
                if r_type == 'SINGLE':
                    multiplier = 0.8
                elif r_type == 'DOUBLE':
                    multiplier = 1.2
                elif r_type == 'SUITE':
                    multiplier = 2.5
                elif r_type == 'DELUXE':
                    multiplier = 1.5
                    
                Room.objects.create(
                    hotel=hotel,
                    room_type=r_type,
                    price_per_night=base_price * multiplier,
                    capacity=1 if r_type == 'SINGLE' else (4 if r_type == 'SUITE' else 2)
                )
            
            self.stdout.write(f"Added Hotel: {hotel.name}")

        self.stdout.write(self.style.SUCCESS("Successfully seeded 7 new Hotels along with their rooms!"))
