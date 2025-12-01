from django.shortcuts import render
from django.db.models import Q
from .models import Hotel

def search_hotels(request):
    query = request.GET.get('city') # Keeping param name 'city' for backward compatibility, but treating as general query
    
    hotels = Hotel.objects.all()

    if query:
        hotels = hotels.filter(Q(city__icontains=query) | Q(name__icontains=query))

    price_range = request.GET.get('price_range')
    if price_range:
        if price_range == 'low':
            hotels = hotels.filter(rooms__price_per_night__lt=10000).distinct()
        elif price_range == 'mid':
            hotels = hotels.filter(rooms__price_per_night__gte=10000, rooms__price_per_night__lte=50000).distinct()
        elif price_range == 'high':
            hotels = hotels.filter(rooms__price_per_night__gt=50000).distinct()

    # Get unique cities from hotels
    cities = Hotel.objects.values_list('city', flat=True).distinct().order_by('city')
    
    context = {
        'hotels': hotels,
        'city_query': query,
        'cities': cities,
    }
    return render(request, 'hotels/search_results.html', context)
