# ==========================================
# PACKAGES APP VIEWS
# ==========================================
# This file contains the logic for browsing and displaying holiday packages.
# Features included: Package Search Engine and Package Details Page.

from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import Package

# ---------------------------------------------------------
# 1. SEARCH PACKAGES VIEW
# ---------------------------------------------------------
# Handles queries for tour packages by destination/title and filters by price.
def search_packages(request):
    query = request.GET.get('destination') # Keeping param name 'destination' but treating as general query
    price_range = request.GET.get('price_range')
    packages = Package.objects.all()

    if query:
        packages = packages.filter(Q(destination__icontains=query) | Q(title__icontains=query))

    if price_range:
        if price_range == 'low':
            packages = packages.filter(price__lt=10000)
        elif price_range == 'mid':
            packages = packages.filter(price__gte=10000, price__lte=50000)
        elif price_range == 'high':
            packages = packages.filter(price__gt=50000)

    return render(request, 'packages/search_results.html', {'packages': packages})

# ---------------------------------------------------------
# 2. PACKAGE DETAIL VIEW
# ---------------------------------------------------------
# Displays in-depth information about a specific holiday package, including itinerary.
def package_detail(request, pk):
    package = get_object_or_404(Package, pk=pk)
    return render(request, 'packages/package_detail.html', {'package': package})
