from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DetailView, DeleteView
from django.urls import reverse_lazy
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from django.db.models import Sum
from bookings.models import Booking
from flights.models import Flight
from hotels.models import Hotel
from packages.models import Package
from bookings.models import Payment
from django.contrib.auth import get_user_model
from .forms import FlightForm, HotelForm, PackageForm, BookingStatusForm

User = get_user_model()

from django.core.cache import cache

# ==========================================
# 1. DASHBOARD OVERVIEW
# ==========================================
# Handles the main dashboard page, compiling metrics and recent activities.

@method_decorator(staff_member_required, name='dispatch')
class DashboardHomeView(TemplateView):
    template_name = 'dashboard/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Overview'
        
        # Cache metrics for 5 minutes (300 seconds)
        metrics = cache.get('dashboard_metrics')
        
        if not metrics:
            revenue = Booking.objects.filter(status='CONFIRMED').aggregate(Sum('total_price'))['total_price__sum']
            metrics = {
                'total_revenue': revenue if revenue else 0,
                'active_bookings': Booking.objects.filter(status='CONFIRMED').count(),
                'pending_bookings': Booking.objects.filter(status='PENDING').count(),
                'total_customers': User.objects.filter(is_staff=False).count(),
            }
            cache.set('dashboard_metrics', metrics, 300)
            
        context.update(metrics)
        
        # Recent Bookings (Last 5) - Fix N+1 Query
        context['recent_bookings'] = Booking.objects.select_related(
            'user', 'flight__origin', 'flight__destination', 'room__hotel', 'package'
        ).order_by('-booking_date')[:5]
        
        return context

# ==========================================
# 2. BOOKINGS MANAGEMENT
# ==========================================
# Views for listing, viewing details, updating status, and deleting bookings.

@method_decorator(staff_member_required, name='dispatch')
class BookingListView(ListView):
    model = Booking
    template_name = 'dashboard/booking_list.html'
    context_object_name = 'bookings'
    ordering = ['-booking_date']
    paginate_by = 10

    def get_queryset(self):
        # Fix N+1 Query
        queryset = super().get_queryset().select_related(
            'user', 'flight__origin', 'flight__destination', 'room__hotel', 'package'
        )
        
        # Search by ID, Email, or Username
        q = self.request.GET.get('q')
        if q:
            if q.isdigit():
                queryset = queryset.filter(id=q)
            else:
                from django.db.models import Q
                queryset = queryset.filter(
                    Q(user__email__icontains=q) | 
                    Q(user__username__icontains=q) |
                    Q(user__first_name__icontains=q) |
                    Q(user__last_name__icontains=q)
                )
                
        # Filter by Status
        status = self.request.GET.get('status')
        if status:
            queryset = queryset.filter(status=status)
            
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'All Bookings'
        
        # Pass current filters to context
        context['current_q'] = self.request.GET.get('q', '')
        context['current_status'] = self.request.GET.get('status', '')
        
        return context

@method_decorator(staff_member_required, name='dispatch')
class BookingDetailView(DetailView):
    model = Booking
    template_name = 'dashboard/booking_detail.html'
    context_object_name = 'booking'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Booking #{self.object.id} Details'
        return context

@method_decorator(staff_member_required, name='dispatch')
class BookingUpdateView(UpdateView):
    model = Booking
    form_class = BookingStatusForm
    template_name = 'dashboard/generic_form.html'
    success_url = reverse_lazy('dashboard:booking_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Update Status for Booking #{self.object.id}'
        context['cancel_url'] = reverse_lazy('dashboard:booking_list')
        return context

@method_decorator(staff_member_required, name='dispatch')
class BookingDeleteView(DeleteView):
    model = Booking
    template_name = 'dashboard/booking_confirm_delete.html'
    success_url = reverse_lazy('dashboard:booking_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Delete Booking'
        return context

# ==========================================
# 3. FLIGHTS MANAGEMENT
# ==========================================
# Views for listing, creating, and updating flight schedules.

@method_decorator(staff_member_required, name='dispatch')
class FlightListView(ListView):
    model = Flight
    template_name = 'dashboard/flight_list.html'
    context_object_name = 'flights'
    ordering = ['-departure_time']
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Flights Schedule'
        return context

from .forms import FlightForm

@method_decorator(staff_member_required, name='dispatch')
class FlightCreateView(CreateView):
    model = Flight
    form_class = FlightForm
    template_name = 'dashboard/flight_form.html'
    success_url = reverse_lazy('dashboard:flight_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Add New Flight'
        return context

@method_decorator(staff_member_required, name='dispatch')
class FlightUpdateView(UpdateView):
    model = Flight
    form_class = FlightForm
    template_name = 'dashboard/flight_form.html'
    success_url = reverse_lazy('dashboard:flight_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edit Flight'
        return context

# ==========================================
# 4. PAYMENTS MANAGEMENT
# ==========================================
# View for listing and reviewing transaction histories.

@method_decorator(staff_member_required, name='dispatch')
class PaymentListView(ListView):
    model = Payment
    template_name = 'dashboard/payment_list.html'
    context_object_name = 'payments'
    ordering = ['-timestamp']
    paginate_by = 10

    def get_queryset(self):
        return super().get_queryset().select_related('booking__user')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Payments History'
        return context

# ==========================================
# 5. HOTELS MANAGEMENT
# ==========================================
# Views for listing, creating, and updating hotels.

@method_decorator(staff_member_required, name='dispatch')
class HotelListView(ListView):
    model = Hotel
    template_name = 'dashboard/hotel_list.html'
    context_object_name = 'hotels'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Hotels Management'
        return context

@method_decorator(staff_member_required, name='dispatch')
class HotelCreateView(CreateView):
    model = Hotel
    form_class = HotelForm
    template_name = 'dashboard/generic_form.html'
    success_url = reverse_lazy('dashboard:hotel_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Add New Hotel'
        context['cancel_url'] = reverse_lazy('dashboard:hotel_list')
        return context

@method_decorator(staff_member_required, name='dispatch')
class HotelUpdateView(UpdateView):
    model = Hotel
    form_class = HotelForm
    template_name = 'dashboard/generic_form.html'
    success_url = reverse_lazy('dashboard:hotel_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edit Hotel'
        context['cancel_url'] = reverse_lazy('dashboard:hotel_list')
        return context

# ==========================================
# 6. HOLIDAY PACKAGES MANAGEMENT
# ==========================================
# Views for listing, creating, and updating travel packages.

@method_decorator(staff_member_required, name='dispatch')
class PackageListView(ListView):
    model = Package
    template_name = 'dashboard/package_list.html'
    context_object_name = 'packages'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Holiday Packages'
        return context

@method_decorator(staff_member_required, name='dispatch')
class PackageCreateView(CreateView):
    model = Package
    form_class = PackageForm
    template_name = 'dashboard/generic_form.html'
    success_url = reverse_lazy('dashboard:package_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Add New Package'
        context['cancel_url'] = reverse_lazy('dashboard:package_list')
        return context

@method_decorator(staff_member_required, name='dispatch')
class PackageUpdateView(UpdateView):
    model = Package
    form_class = PackageForm
    template_name = 'dashboard/generic_form.html'
    success_url = reverse_lazy('dashboard:package_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edit Package'
        context['cancel_url'] = reverse_lazy('dashboard:package_list')
        return context

# ==========================================
# 7. CUSTOMERS MANAGEMENT
# ==========================================
# View for listing registered customers in the system.

@method_decorator(staff_member_required, name='dispatch')
class CustomerListView(ListView):
    model = User
    template_name = 'dashboard/customer_list.html'
    context_object_name = 'customers'
    ordering = ['-date_joined']
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Customers'
        return context

@method_decorator(staff_member_required, name='dispatch')
class CustomerDetailView(DetailView):
    model = User
    template_name = 'dashboard/customer_profile.html'
    context_object_name = 'customer'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        customer = self.object
        context['title'] = 'Customer Profile'
        
        # Add profile to context explicitly to avoid DoesNotExist template errors
        profile = getattr(customer, 'profile', None)
        context['profile'] = profile
        
        # Fetch bookings
        bookings = Booking.objects.filter(user=customer).order_by('-booking_date')
        context['bookings'] = bookings
        
        # Fetch payments
        payments = Payment.objects.filter(booking__user=customer).order_by('-timestamp')
        context['payments'] = payments
        
        # Calculate total amount spent (only completed payments)
        total_spent = payments.filter(status='COMPLETED').aggregate(total=Sum('amount'))['total'] or 0
        context['total_spent'] = total_spent
        
        return context

@staff_member_required
def customer_toggle_status(request, pk):
    customer = get_object_or_404(User, pk=pk)
    if not customer.is_superuser:  # Prevent suspending superusers
        customer.is_active = not customer.is_active
        customer.save()
    return redirect('dashboard:customer_profile', pk=customer.pk)

@method_decorator(staff_member_required, name='dispatch')
class CustomerDeleteView(DeleteView):
    model = User
    template_name = 'dashboard/customer_confirm_delete.html'
    success_url = reverse_lazy('dashboard:customer_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Delete Customer'
        return context
