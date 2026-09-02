# ==========================================
# BOOKINGS APP VIEWS
# ==========================================
# This file contains the logic for creating, managing, and finalizing bookings.
# Features included: Checkout, Payment Processing (SSLCommerz), My Bookings, and Ticket Printing.

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .models import Booking
from flights.models import Flight
from hotels.models import Room
from packages.models import Package


from .models import Payment
import logging
from django_ratelimit.decorators import ratelimit

logger = logging.getLogger(__name__)

import uuid
import requests
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

# ---------------------------------------------------------
# 1. CREATE BOOKING
# ---------------------------------------------------------
# Initiates a new booking for flights, hotels, or packages and prepares payment context.
@login_required
@ratelimit(key='user', rate='5/m', block=True)
def create_booking(request, type, id):
    # Identify the object being booked
    if type == 'flight':
        model = Flight
        obj = get_object_or_404(Flight, id=id)
        price = obj.price
        summary = f"Flight: {obj.airline.name} ({obj.origin.code} to {obj.destination.code})"
    elif type == 'hotel':
        model = Room
        obj = get_object_or_404(Room, id=id)
        price = obj.price_per_night
        summary = f"Hotel: {obj.hotel.name} - {obj.get_room_type_display()}"
    elif type == 'package':
        model = Package
        obj = get_object_or_404(Package, id=id)
        price = obj.price
        summary = f"Package: {obj.title} ({obj.duration_days} Days)"
    else:
        return redirect('home')

    if request.method == 'POST':
        # 1. Create Pending Booking
        booking = Booking.objects.create(
            user=request.user,
            total_price=price,
            status='PENDING'
        )
        if type == 'flight':
            booking.flight = obj
        elif type == 'hotel':
            booking.room = obj
        elif type == 'package':
            booking.package = obj
        booking.save()

        # 2. Create Pending Payment
        tran_id = f"FLYNOVA_{booking.id}_{uuid.uuid4().hex[:8].upper()}"
        payment = Payment.objects.create(
            booking=booking,
            payment_method='SSLCOMMERZ',
            amount=price,
            transaction_id=tran_id,
            status='PENDING'
        )

        # 3. Initialize SSLCommerz
        store_id = settings.SSLCOMMERZ_STORE_ID
        store_pass = settings.SSLCOMMERZ_STORE_PASSWORD
        is_sandbox = settings.SSLCOMMERZ_IS_SANDBOX

        base_url = "https://sandbox.sslcommerz.com" if is_sandbox else "https://securepay.sslcommerz.com"
        init_url = f"{base_url}/gwprocess/v4/api.php"
        
        host = request.build_absolute_uri('/')[:-1]
        
        post_body = {
            'store_id': store_id,
            'store_passwd': store_pass,
            'total_amount': price,
            'currency': 'BDT',
            'tran_id': tran_id,
            'success_url': f"{host}{reverse('sslcommerz_success')}",
            'fail_url': f"{host}{reverse('sslcommerz_fail')}",
            'cancel_url': f"{host}{reverse('sslcommerz_cancel')}",
            'emi_option': 0,
            'cus_name': request.user.get_full_name() or request.user.username,
            'cus_email': request.user.email,
            'cus_phone': '01700000000',
            'cus_add1': 'Dhaka',
            'cus_city': 'Dhaka',
            'cus_country': 'Bangladesh',
            'shipping_method': 'NO',
            'product_name': summary,
            'product_category': type,
            'product_profile': 'general',
        }
        
        try:
            response = requests.post(init_url, data=post_body)
            response_data = response.json()
            if response_data.get('status') == 'SUCCESS':
                gateway_url = response_data['GatewayPageURL']
                return redirect(gateway_url)
            else:
                messages.error(request, f"Payment gateway error: {response_data.get('failedreason', 'Unknown error')}")
                return redirect('home')
        except Exception as e:
            logger.error(f"SSLCommerz Init Error: {e}")
            messages.error(request, "Failed to connect to the payment gateway.")
            return redirect('home')

    context = {
        'object': obj,
        'type': type,
        'price': price,
        'summary': summary,
    }
    return render(request, 'bookings/checkout.html', context)

# ---------------------------------------------------------
# 2. SSLCOMMERZ SUCCESS CALLBACK
# ---------------------------------------------------------
# Handles successful payment responses from the SSLCommerz gateway.
@csrf_exempt
def sslcommerz_success(request):
    if request.method == 'POST':
        tran_id = request.POST.get('tran_id')
        val_id = request.POST.get('val_id')
        bank_tran_id = request.POST.get('bank_tran_id')
        card_type = request.POST.get('card_type')
        status = request.POST.get('status')

        if status == 'VALID':
            try:
                payment = Payment.objects.get(transaction_id=tran_id)
                booking = payment.booking
                
                # Update Payment
                payment.status = 'SUCCESS'
                payment.val_id = val_id
                payment.bank_tran_id = bank_tran_id
                payment.payment_method = card_type if card_type else 'SSLCOMMERZ'
                payment.save()
                
                # Update Booking
                booking.status = 'CONFIRMED'
                booking.save()
                
                # Send Email Asynchronously
                subject = f'Booking Confirmation - #{booking.id}'
                message = f'''Hi {booking.user.username},

Your payment of BDT {payment.amount} was successful.
Your booking is confirmed.

Thank you for choosing FlyNova!'''
                from_email = settings.EMAIL_HOST_USER
                recipient_list = [booking.user.email]
                
                import threading
                def send_email_async(subject, message, from_email, recipient_list):
                    try:
                        send_mail(subject, message, from_email, recipient_list, fail_silently=False)
                    except Exception as e:
                        logger.error(f"Email sending failed: {e}")
                
                email_thread = threading.Thread(target=send_email_async, args=(subject, message, from_email, recipient_list))
                email_thread.start()
                
                messages.success(request, f"Payment Successful! Booking Confirmed (ID #{booking.id})")
                return redirect('booking_success', pk=booking.id)
            except Payment.DoesNotExist:
                messages.error(request, "Payment record not found.")
                return redirect('home')
    
    return redirect('home')

# ---------------------------------------------------------
# 3. SSLCOMMERZ FAILURE CALLBACK
# ---------------------------------------------------------
# Handles failed payment responses from the SSLCommerz gateway.
@csrf_exempt
def sslcommerz_fail(request):
    if request.method == 'POST':
        tran_id = request.POST.get('tran_id')
        try:
            payment = Payment.objects.get(transaction_id=tran_id)
            payment.status = 'FAILED'
            payment.save()
            
            booking = payment.booking
            booking.status = 'CANCELLED'
            booking.save()
        except Payment.DoesNotExist:
            pass
            
    messages.error(request, "Payment Failed. Your booking was not confirmed.")
    return redirect('home')

# ---------------------------------------------------------
# 4. SSLCOMMERZ CANCEL CALLBACK
# ---------------------------------------------------------
# Handles cancelled payment responses from the SSLCommerz gateway.
@csrf_exempt
def sslcommerz_cancel(request):
    if request.method == 'POST':
        tran_id = request.POST.get('tran_id')
        try:
            payment = Payment.objects.get(transaction_id=tran_id)
            payment.status = 'CANCELLED'
            payment.save()
            
            booking = payment.booking
            booking.status = 'CANCELLED'
            booking.save()
        except Payment.DoesNotExist:
            pass
            
    messages.warning(request, "Payment was cancelled.")
    return redirect('home')

# ---------------------------------------------------------
# 5. BOOKING SUCCESS PAGE
# ---------------------------------------------------------
# Displays a confirmation page to the user after a successful booking.
@login_required
def booking_success(request, pk):
    booking = get_object_or_404(Booking, pk=pk, user=request.user)
    return render(request, 'bookings/success.html', {'booking': booking})

# ---------------------------------------------------------
# 6. MY BOOKINGS DASHBOARD
# ---------------------------------------------------------
# Shows a list of all bookings made by the logged-in user.
@login_required
def my_bookings(request):
    bookings = Booking.objects.filter(user=request.user).prefetch_related('flight', 'room', 'package').order_by('-booking_date')
    return render(request, 'bookings/my_bookings.html', {'bookings': bookings})

# ---------------------------------------------------------
# 7. PRINT TICKET (HTML)
# ---------------------------------------------------------
# Renders a printable HTML view of the booking ticket.
@login_required
def print_ticket(request, pk):
    booking = get_object_or_404(Booking, pk=pk, user=request.user)
    return render(request, 'bookings/print_ticket.html', {'booking': booking})

# ---------------------------------------------------------
# 8. DOWNLOAD TICKET (PDF)
# ---------------------------------------------------------
# Generates and downloads a PDF version of the booking ticket.
@login_required
def download_ticket_pdf(request, pk):
    from django.http import HttpResponse
    from reportlab.lib.pagesizes import letter
    from reportlab.lib import colors
    from reportlab.lib.units import inch
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.enums import TA_CENTER
    import io
    
    booking = get_object_or_404(Booking, pk=pk, user=request.user)
    
    try:
        # Create PDF in memory
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        elements = []
        styles = getSampleStyleSheet()
        
        # Custom styles
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#2c7a9e'),
            spaceAfter=30,
            alignment=TA_CENTER
        )
        
        # Title
        title = Paragraph("FlyNova - Booking Confirmation", title_style)
        elements.append(title)
        elements.append(Spacer(1, 0.3*inch))
        
        # Booking Details Table
        booking_data = [
            ['Booking ID:', f'#{booking.id}'],
            ['Passenger Name:', booking.user.get_full_name() or booking.user.username],
            ['Email:', booking.user.email],
            ['Booking Date:', booking.booking_date.strftime('%d %B, %Y')],
            ['Status:', booking.status],
        ]
        
        # Get booking details based on type
        if booking.flight:
            obj = booking.flight
            booking_data.extend([
                ['Type:', 'Flight'],
                ['Airline:', obj.airline.name],
                ['Flight Number:', obj.flight_number],
                ['From:', f"{obj.origin.city} ({obj.origin.code})"],
                ['To:', f"{obj.destination.city} ({obj.destination.code})"],
                ['Departure:', obj.departure_time.strftime('%d %B, %Y at %H:%M')],
                ['Arrival:', obj.arrival_time.strftime('%d %B, %Y at %H:%M')],
            ])
        elif booking.package:
            obj = booking.package
            booking_data.extend([
                ['Type:', 'Package'],
                ['Package:', obj.title],
                ['Destination:', obj.destination],
                ['Duration:', f"{obj.duration_days} Days / {obj.duration_nights} Nights"],
            ])
        elif booking.room:
            obj = booking.room
            booking_data.extend([
                ['Type:', 'Hotel'],
                ['Hotel:', obj.hotel.name],
                ['Room Type:', obj.get_room_type_display()],
                ['Location:', obj.hotel.city],
            ])
        
        booking_data.append(['Total Price:', f'BDT {booking.total_price}'])
        
        # Create table
        table = Table(booking_data, colWidths=[2*inch, 4*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f0f0f0')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 11),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('TOPPADDING', (0, 0), (-1, -1), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
        ]))
        
        elements.append(table)
        elements.append(Spacer(1, 0.5*inch))
        
        # Footer
        footer_text = Paragraph(
            "<b>Thank you for choosing FlyNova!</b><br/>For any queries, contact us at support@flynova.com",
            styles['Normal']
        )
        elements.append(footer_text)
        
        # Build PDF
        doc.build(elements)
        
        # Get PDF from buffer
        pdf = buffer.getvalue()
        buffer.close()
        
        # Create response
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="FlyNova_Ticket_{booking.id}.pdf"'
        response.write(pdf)
        
        return response
    except Exception as e:
        return HttpResponse(f"Error generating PDF: {str(e)}", status=500)
