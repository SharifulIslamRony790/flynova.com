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

@login_required
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
        # Create the booking
        booking = Booking.objects.create(
            user=request.user,
            content_type=ContentType.objects.get_for_model(model),
            object_id=obj.id,
            total_price=price,
            status='CONFIRMED'
        )
        
        # Send Email
        subject = f'Booking Confirmation - #{booking.id}'
        message = f'Hi {request.user.username},\\n\\nYour booking for {summary} has been confirmed.\\nTotal Price: BDT {price}\\n\\nThank you for choosing FlyNova!'
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [request.user.email]
        
        send_mail(subject, message, from_email, recipient_list, fail_silently=True)
        
        messages.success(request, f"Booking Successful! Your Booking ID is #{booking.id}")
        return redirect('booking_success', pk=booking.id)

    context = {
        'object': obj,
        'type': type,
        'price': price,
        'summary': summary
    }
    return render(request, 'bookings/checkout.html', context)

@login_required
def booking_success(request, pk):
    booking = get_object_or_404(Booking, pk=pk, user=request.user)
    return render(request, 'bookings/success.html', {'booking': booking})

@login_required
def my_bookings(request):
    bookings = Booking.objects.filter(user=request.user).order_by('-booking_date')
    return render(request, 'bookings/my_bookings.html', {'bookings': bookings})

@login_required
def print_ticket(request, pk):
    booking = get_object_or_404(Booking, pk=pk, user=request.user)
    return render(request, 'bookings/print_ticket.html', {'booking': booking})

@login_required
def download_ticket_pdf(request, pk):
    from django.http import HttpResponse
    from reportlab.lib.pagesizes import letter
    from reportlab.lib import colors
    from reportlab.lib.units import inch
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
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

@login_required
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
        # Create the booking
        booking = Booking.objects.create(
            user=request.user,
            content_type=ContentType.objects.get_for_model(model),
            object_id=obj.id,
            total_price=price,
            status='CONFIRMED'
        )
        
        # Send Email
        subject = f'Booking Confirmation - #{booking.id}'
        message = f'Hi {request.user.username},\\n\\nYour booking for {summary} has been confirmed.\\nTotal Price: BDT {price}\\n\\nThank you for choosing FlyNova!'
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [request.user.email]
        
        send_mail(subject, message, from_email, recipient_list, fail_silently=True)
        
        messages.success(request, f"Booking Successful! Your Booking ID is #{booking.id}")
        return redirect('booking_success', pk=booking.id)

    context = {
        'object': obj,
        'type': type,
        'price': price,
        'summary': summary
    }
    return render(request, 'bookings/checkout.html', context)

@login_required
def booking_success(request, pk):
    booking = get_object_or_404(Booking, pk=pk, user=request.user)
    return render(request, 'bookings/success.html', {'booking': booking})

@login_required
def my_bookings(request):
    bookings = Booking.objects.filter(user=request.user).order_by('-booking_date')
    return render(request, 'bookings/my_bookings.html', {'bookings': bookings})

@login_required
def print_ticket(request, pk):
    booking = get_object_or_404(Booking, pk=pk, user=request.user)
    return render(request, 'bookings/print_ticket.html', {'booking': booking})

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
        if booking.content_object:
            obj = booking.content_object
            if hasattr(obj, 'airline'):  # Flight
                booking_data.extend([
                    ['Type:', 'Flight'],
                    ['Airline:', obj.airline.name],
                    ['Flight Number:', obj.flight_number],
                    ['From:', f"{obj.origin.city} ({obj.origin.code})"],
                    ['To:', f"{obj.destination.city} ({obj.destination.code})"],
                    ['Departure:', obj.departure_time.strftime('%d %B, %Y at %H:%M')],
                    ['Arrival:', obj.arrival_time.strftime('%d %B, %Y at %H:%M')],
                ])
            elif hasattr(obj, 'title'):  # Package
                booking_data.extend([
                    ['Type:', 'Package'],
                    ['Package:', obj.title],
                    ['Destination:', obj.destination],
                    ['Duration:', f"{obj.duration_days} Days / {obj.duration_nights} Nights"],
                ])
            elif hasattr(obj, 'hotel'):  # Hotel
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
