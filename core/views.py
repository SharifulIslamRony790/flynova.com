from django.shortcuts import render
from flights.models import Airport

def home(request):
    airports = Airport.objects.all().order_by('city')
    return render(request, 'core/home.html', {'airports': airports})
