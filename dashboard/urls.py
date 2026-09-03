from django.urls import path
from . import views

# ==========================================
# DASHBOARD APP URL CONFIGURATION
# ==========================================
# This file maps URL patterns to their respective views for the admin dashboard.
# Features included: Dashboard Home, Bookings, Flights, Payments, Hotels, Packages, Customers

app_name = 'dashboard'

urlpatterns = [
    # ---------------------------------------------------------
    # 1. CORE DASHBOARD
    # ---------------------------------------------------------
    path('', views.DashboardHomeView.as_view(), name='home'),

    # ---------------------------------------------------------
    # 2. BOOKINGS MANAGEMENT (View, Update, Delete)
    # ---------------------------------------------------------
    path('bookings/', views.BookingListView.as_view(), name='booking_list'),
    path('bookings/<int:pk>/', views.BookingDetailView.as_view(), name='booking_detail'),
    path('bookings/<int:pk>/edit/', views.BookingUpdateView.as_view(), name='booking_update'),
    path('bookings/<int:pk>/delete/', views.BookingDeleteView.as_view(), name='booking_delete'),
    
    # ---------------------------------------------------------
    # 3. FLIGHTS MANAGEMENT (CRUD)
    # ---------------------------------------------------------
    path('flights/', views.FlightListView.as_view(), name='flight_list'),
    path('flights/add/', views.FlightCreateView.as_view(), name='flight_create'),
    path('flights/<int:pk>/edit/', views.FlightUpdateView.as_view(), name='flight_update'),
    path('flights/<int:pk>/delete/', views.FlightDeleteView.as_view(), name='flight_delete'),
    
    # ---------------------------------------------------------
    # 4. PAYMENTS MANAGEMENT
    # ---------------------------------------------------------
    path('payments/', views.PaymentListView.as_view(), name='payment_list'),
    
    # ---------------------------------------------------------
    # 5. HOTELS MANAGEMENT (CRUD)
    # ---------------------------------------------------------
    path('hotels/', views.HotelListView.as_view(), name='hotel_list'),
    path('hotels/add/', views.HotelCreateView.as_view(), name='hotel_create'),
    path('hotels/<int:pk>/edit/', views.HotelUpdateView.as_view(), name='hotel_update'),
    path('hotels/<int:pk>/delete/', views.HotelDeleteView.as_view(), name='hotel_delete'),
    
    # ---------------------------------------------------------
    # 6. HOLIDAY PACKAGES MANAGEMENT (CRUD)
    # ---------------------------------------------------------
    path('packages/', views.PackageListView.as_view(), name='package_list'),
    path('packages/add/', views.PackageCreateView.as_view(), name='package_create'),
    path('packages/<int:pk>/edit/', views.PackageUpdateView.as_view(), name='package_update'),
    path('packages/<int:pk>/delete/', views.PackageDeleteView.as_view(), name='package_delete'),
    
    # ---------------------------------------------------------
    # 7. CUSTOMERS MANAGEMENT
    # ---------------------------------------------------------
    path('customers/', views.CustomerListView.as_view(), name='customer_list'),
    path('customers/<int:pk>/', views.CustomerDetailView.as_view(), name='customer_profile'),
    path('customers/<int:pk>/toggle-status/', views.customer_toggle_status, name='customer_toggle_status'),
    path('customers/<int:pk>/delete/', views.CustomerDeleteView.as_view(), name='customer_delete'),
]
