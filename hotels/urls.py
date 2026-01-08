from django.urls import path
from . import views

urlpatterns = [
    path('', views.search_hotels, name='hotels'),  # Root URL for hotels
    path('search/', views.search_hotels, name='search_hotels'),
]

