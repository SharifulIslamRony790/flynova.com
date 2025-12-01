from django.urls import path
from . import views

urlpatterns = [
    path('search/', views.search_flights, name='search_flights'),
    path('airport-info/', views.airport_info, name='airport_info'),
]
