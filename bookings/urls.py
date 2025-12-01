from django.urls import path
from . import views

urlpatterns = [
    path('create/<str:type>/<int:id>/', views.create_booking, name='create_booking'),
    path('success/<int:pk>/', views.booking_success, name='booking_success'),
    path('my-bookings/', views.my_bookings, name='my_bookings'),
    path('print/<int:pk>/', views.print_ticket, name='print_ticket'),
    path('download-pdf/<int:pk>/', views.download_ticket_pdf, name='download_ticket_pdf'),
]
