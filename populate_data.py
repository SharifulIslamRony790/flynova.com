import os
import django
from django.utils import timezone
from datetime import timedelta, datetime, timezone as dt_timezone
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from flights.models import Flight, Airport, Airline
from hotels.models import Hotel, Room
from packages.models import Package, Itinerary

def create_flight_data():
    print("Creating Airport Data (Bangladesh Only)...")
    airports = [
        {'code': 'DAC', 'name': 'Hazrat Shahjalal International Airport', 'city': 'Dhaka', 'country': 'Bangladesh'},
        {'code': 'CXB', 'name': "Cox's Bazar Airport", 'city': "Cox's Bazar", 'country': 'Bangladesh'},
        {'code': 'CGP', 'name': 'Shah Amanat International Airport', 'city': 'Chittagong', 'country': 'Bangladesh'},
        {'code': 'JSR', 'name': 'Jashore Airport', 'city': 'Jashore', 'country': 'Bangladesh'},
        {'code': 'SPD', 'name': 'Saidpur Airport', 'city': 'Saidpur', 'country': 'Bangladesh'},
        {'code': 'ZYL', 'name': 'Osmani International Airport', 'city': 'Sylhet', 'country': 'Bangladesh'},
    ]

    airport_objs = {}
    for apt in airports:
        obj, created = Airport.objects.get_or_create(code=apt['code'], defaults=apt)
        airport_objs[apt['code']] = obj
        if created: print(f"Created {apt['name']}")

    print("Creating Airline Data...")
    airlines = ['Biman Bangladesh', 'US-Bangla Airlines', 'Novoair', 'Regent Airways']
    airline_objs = []
    for name in airlines:
        obj, created = Airline.objects.get_or_create(name=name)
        airline_objs.append(obj)
        if created: print(f"Created {name}")

    print("Creating Flight Schedules (Bangladesh Domestic)...")
    today = timezone.now().date()
    
    # Clear existing flights
    Flight.objects.all().delete()
    
    routes = [
        ('DAC', 'CXB', 'US-Bangla Airlines', 4500, '10:00', '11:00'),
        ('DAC', 'CXB', 'Novoair', 4800, '14:00', '15:00'),
        ('DAC', 'CGP', 'Biman Bangladesh', 3500, '09:00', '10:00'),
        ('DAC', 'CGP', 'US-Bangla Airlines', 3200, '16:00', '17:00'),
        ('DAC', 'JSR', 'Novoair', 2800, '11:00', '12:00'),
        ('DAC', 'SPD', 'Regent Airways', 4000, '08:00', '09:30'),
        ('DAC', 'ZYL', 'Biman Bangladesh', 3800, '15:00', '16:00'),
        ('CXB', 'DAC', 'US-Bangla Airlines', 4500, '12:00', '13:00'),
        ('CGP', 'DAC', 'Biman Bangladesh', 3500, '11:00', '12:00'),
        ('ZYL', 'DAC', 'Novoair', 3800, '17:00', '18:00'),
    ]
    
    for i in range(30):  # Next 30 days
        date = today + timedelta(days=i)
        
        for origin, dest, airline_name, price, dep_time, arr_time in routes:
            Flight.objects.create(
                airline=Airline.objects.get(name=airline_name),
                flight_number=f'{airline_name[:2].upper()}-{random.randint(100, 999)}',
                origin=airport_objs[origin],
                destination=airport_objs[dest],
                departure_time=datetime.combine(date, datetime.strptime(dep_time, "%H:%M").time()).replace(tzinfo=dt_timezone.utc),
                arrival_time=datetime.combine(date, datetime.strptime(arr_time, "%H:%M").time()).replace(tzinfo=dt_timezone.utc),
                price=price
            )

    print(f"Created {Flight.objects.count()} flights!")

def create_hotel_data():
    print("Creating Hotel Data (Bangladesh)...")
    hotels = [
        {
            'name': 'Sea Pearl Beach Resort',
            'city': "Cox's Bazar",
            'address': "Inani Beach, Cox's Bazar",
            'description': '5-star luxury resort with sea view.',
            'star_rating': 5,
            'image': 'hotels/photo-1445019980597-93fa8acb246c.jpg'
        },
        {
            'name': 'Hotel The Cox Today',
            'city': "Cox's Bazar",
            'address': "Kolatoli Road, Cox's Bazar",
            'description': 'Premium hotel near the beach.',
            'star_rating': 4,
            'image': 'hotels/photo-1542314831-068cd1dbfeeb.jpg'
        },
        {
            'name': 'Pan Pacific Sonargaon',
            'city': 'Dhaka',
            'address': 'Karwan Bazar, Dhaka',
            'description': 'Luxury hotel in the heart of Dhaka.',
            'star_rating': 5,
            'image': 'hotels/photo-1566073771259-6a8506099945.jpg'
        },
        {
            'name': 'Hotel Agrabad',
            'city': 'Chittagong',
            'address': 'Agrabad, Chittagong',
            'description': 'Business hotel in Chittagong.',
            'star_rating': 4,
            'image': 'hotels/photo-1571896349842-33c89424de2d (1).jpg'
        },
        {
            'name': 'Grand Sultan Tea Resort',
            'city': 'Sylhet',
            'address': 'Sreemangal, Sylhet',
            'description': 'Tea garden resort in Sylhet.',
            'star_rating': 4,
            'image': 'hotels/photo-1445019980597-93fa8acb246c.jpg'
        }
    ]

    for h_data in hotels:
        hotel, created = Hotel.objects.update_or_create(name=h_data['name'], defaults=h_data)
        if created:
            print(f"Created {hotel.name}")
            Room.objects.get_or_create(hotel=hotel, room_type='SINGLE', defaults={'price_per_night': 3000, 'capacity': 1})
            Room.objects.get_or_create(hotel=hotel, room_type='DOUBLE', defaults={'price_per_night': 5000, 'capacity': 2})
            Room.objects.get_or_create(hotel=hotel, room_type='SUITE', defaults={'price_per_night': 10000, 'capacity': 4})
        else:
            print(f"Updated {hotel.name}")

    print("Hotel Data Created Successfully!")

def create_package_data():
    print("Creating Package Data (Bangladesh)...")
    packages = [
        {
            'title': "Cox's Bazar Beach Holiday",
            'destination': "Cox's Bazar",
            'duration_days': 3,
            'duration_nights': 2,
            'price': 15000.00,
            'overview': "Enjoy the world's longest natural sea beach with hotel and sightseeing.",
            'image': 'packages/photo-1506905925346-21bda4d32df4 (1).jpg'
        },
        {
            'title': 'Sylhet Tea Garden Tour',
            'destination': 'Sylhet',
            'duration_days': 4,
            'duration_nights': 3,
            'price': 12000.00,
            'overview': 'Explore the beautiful tea gardens and waterfalls of Sylhet.',
            'image': 'packages/photo-1506905925346-21bda4d32df4.jpg'
        },
        {
            'title': 'Sundarbans Mangrove Forest',
            'destination': 'Khulna',
            'duration_days': 3,
            'duration_nights': 2,
            'price': 18000.00,
            'overview': 'Adventure tour to the largest mangrove forest and Royal Bengal Tiger habitat.',
            'image': 'packages/photo-1559827260-dc66d52bef19.jpg'
        },
        {
            'title': 'Chittagong Hill Tracts',
            'destination': 'Bandarban',
            'duration_days': 5,
            'duration_nights': 4,
            'price': 20000.00,
            'overview': 'Explore the hills, waterfalls, and tribal culture of Bandarban.',
            'image': 'packages/photo-1564760055775-d63b17a55c44.jpg'
        }
    ]

    for p_data in packages:
        pkg, created = Package.objects.update_or_create(title=p_data['title'], defaults=p_data)
        if created:
            print(f"Created {pkg.title}")
            Itinerary.objects.create(package=pkg, day_number=1, activity='Arrival and Check-in at hotel')
            Itinerary.objects.create(package=pkg, day_number=2, activity='Full day sightseeing tour')
            if p_data['duration_days'] > 3:
                Itinerary.objects.create(package=pkg, day_number=3, activity='Adventure activities and local exploration')
            Itinerary.objects.create(package=pkg, day_number=p_data['duration_days'], activity='Departure')

    print("Package Data Created Successfully!")

def create_superuser():
    from django.contrib.auth import get_user_model
    User = get_user_model()
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'admin@flynova.com', 'admin')
        print("[OK] Superuser 'admin' created (password: admin)")
    else:
        print("[INFO] Superuser 'admin' already exists")

if __name__ == '__main__':
    create_superuser()
    create_flight_data()
    create_hotel_data()
    create_package_data()
    print("\n[SUCCESS] All Bangladesh data created successfully!")
