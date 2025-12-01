
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('accounts/', include('accounts.urls')),
    path('accounts/', include('allauth.urls')),  # Allauth URLs
    path('flights/', include('flights.urls')),
    path('hotels/', include('hotels.urls')),
    path('packages/', include('packages.urls')),
    path('bookings/', include('bookings.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
