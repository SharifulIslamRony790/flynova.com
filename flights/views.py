from django.shortcuts import render
from .models import Flight, Airport

from django.db.models import Q

def search_flights(request):
    origin_code = request.GET.get('origin')
    destination_code = request.GET.get('destination')
    date = request.GET.get('date')
    passengers = request.GET.get('passengers', '1')
    price_filter = request.GET.get('price_filter', 'all')  # New: price filter
    
    try:
        num_passengers = int(passengers)
    except:
        num_passengers = 1

    flights = Flight.objects.all()

    if origin_code:
        flights = flights.filter(Q(origin__code__icontains=origin_code) | Q(origin__city__icontains=origin_code))
    
    if destination_code:
        flights = flights.filter(Q(destination__code__icontains=destination_code) | Q(destination__city__icontains=destination_code))

    if date:
        flights = flights.filter(departure_time__date=date)
    
    # Calculate price categories dynamically
    price_categories = {'low': None, 'mid': None, 'high': None}
    all_prices = list(Flight.objects.values_list('price', flat=True).order_by('price'))
    
    if all_prices:
        # Divide into three equal categories
        count = len(all_prices)
        low_threshold = all_prices[count // 3] if count >= 3 else all_prices[0]
        high_threshold = all_prices[(2 * count) // 3] if count >= 3 else all_prices[-1]
        
        price_categories = {
            'low': low_threshold,
            'mid': high_threshold,
            'high': all_prices[-1]
        }
        
        # Apply price filter
        if price_filter == 'low':
            flights = flights.filter(price__lte=low_threshold)
        elif price_filter == 'mid':
            flights = flights.filter(price__gt=low_threshold, price__lte=high_threshold)
        elif price_filter == 'high':
            flights = flights.filter(price__gt=high_threshold)
    
    # Sort by most recent departure date first
    flights = flights.order_by('-departure_time')
    
    # Add total price for each flight based on passengers
    flights_with_total = []
    for flight in flights:
        flight.total_price = flight.price * num_passengers
        flight.num_passengers = num_passengers
        flights_with_total.append(flight)

    context = {
        'flights': flights_with_total,
        'origin_query': origin_code,
        'destination_query': destination_code,
        'date_query': date,
        'passengers': num_passengers,
        'airports': Airport.objects.all().order_by('city'),
        'price_filter': price_filter,  # Pass current filter to template
        'price_categories': price_categories,  # Pass categories for display
    }
    return render(request, 'flights/search_results.html', context)

def airport_info(request):
    """Display real-time airport information with arriving flights"""
    from django.utils import timezone
    from datetime import timedelta
    
    airports = Airport.objects.all().order_by('city')
    airports_with_arrivals = []
    
    # Get current time and 24 hours from now
    now = timezone.now()
    next_24_hours = now + timedelta(hours=24)
    
    for airport in airports:
        # Get flights arriving at this airport in the next 24 hours
        arrivals = Flight.objects.filter(
            destination=airport,
            arrival_time__gte=now,
            arrival_time__lte=next_24_hours
        ).select_related('airline', 'origin').order_by('arrival_time')
        
        # Add status to each flight
        for flight in arrivals:
            time_until_arrival = (flight.arrival_time - now).total_seconds() / 60  # in minutes
            
            if time_until_arrival < 0:
                flight.status = 'Landed'
            elif time_until_arrival < 30:
                flight.status = 'Landing Soon'
            else:
                flight.status = 'On Time'
        
        if arrivals:
            airports_with_arrivals.append({
                'airport': airport,
                'arrivals': arrivals
            })
    
    context = {
        'airports_with_arrivals': airports_with_arrivals,
    }
    return render(request, 'flights/airport_info.html', context)
