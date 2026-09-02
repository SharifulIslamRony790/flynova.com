# ==========================================
# BOOKINGS APP URL CONFIGURATION
# ==========================================
# This file maps URL patterns for handling bookings and payments.
# Features included: Creating Bookings, Payment Processing (SSLCommerz), My Bookings, and Ticket Printing.

from django.urls import path
from . import views

urlpatterns = [
    # ---------------------------------------------------------
    # 1. BOOKING CREATION
    # ---------------------------------------------------------
    path('create/<str:type>/<int:id>/', views.create_booking, name='create_booking'),
    
    # ---------------------------------------------------------
    # 2. PAYMENT GATEWAY (SSLCommerz)
    # ---------------------------------------------------------
    path('payment/success/', views.sslcommerz_success, name='sslcommerz_success'),
    path('payment/fail/', views.sslcommerz_fail, name='sslcommerz_fail'),
    path('payment/cancel/', views.sslcommerz_cancel, name='sslcommerz_cancel'),
    
    # ---------------------------------------------------------
    # 3. BOOKING MANAGEMENT & TICKETS
    # ---------------------------------------------------------
    path('success/<int:pk>/', views.booking_success, name='booking_success'),
    path('my-bookings/', views.my_bookings, name='my_bookings'),
    path('print/<int:pk>/', views.print_ticket, name='print_ticket'),
    path('download-pdf/<int:pk>/', views.download_ticket_pdf, name='download_ticket_pdf'),
]
