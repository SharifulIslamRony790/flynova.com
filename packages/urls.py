from django.urls import path
from . import views

urlpatterns = [
    path('search/', views.search_packages, name='search_packages'),
    path('<int:pk>/', views.package_detail, name='package_detail'),
]
