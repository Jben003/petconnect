from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.utils import timezone
from .models import Service, Booking
from .forms import ServiceForm, BookingForm


# ==========================
# 🔔 Booking Notification Helpers
# ==========================
def create_booking_notification(booking, message, notification_type='info'):
    """Create notification for booking activities"""
    from adoption.views import create_notification  # Import from adoption views
    
    if notification_type == 'info':
        # Notify shelter about new booking
        create_notification(booking.service.shelter, message, '/services/shelter/bookings/')
    elif notification_type == 'success':
        # Notify adopter about booking updates
        create_notification(booking.adopter, message, '/services/my-bookings/')


def create_booking_request_notification(booking):
    """Notify shelter when a booking is made"""
    message = f"New booking for {booking.service.name} from {booking.adopter.username}"
    create_booking_notification(booking, message, 'info')


def create_booking_confirmed_notification(booking):
    """Notify adopter when booking is confirmed"""
    message = f"Your booking for {booking.service.name} has been confirmed!"
    create_booking_notification(booking, message, 'success')


def create_booking_started_notification(booking):
    """Notify adopter when service starts"""
    message = f"Service {booking.service.name} has started!"
    create_booking_notification(booking, message, 'info')


def create_booking_completed_notification(booking):
    """Notify adopter when service completes"""
    message = f"Service {booking.service.name} has been completed!"
    create_booking_notification(booking, message, 'success')


# ==========================
# 🐾 Service Views
# ==========================
def service_list(request):
    services = Service.objects.filter(is_available=True).order_by('-created_at')

    # Get filter parameters
    search_query = request.GET.get('search', '')
    category = request.GET.get('category', '')
    min_price = request.GET.get('min_price', '')
    max_price = request.GET.get('max_price', '')
    sort_by = request.GET.get('sort_by', 'newest')

    # Search functionality
    if search_query:
        services = services.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query)
        )

    # Filter by category
    if category:
        services = services.filter(category=category)

    # Filter by price range
    if min_price:
        services = services.filter(price__gte=min_price)
    if max_price:
        services = services.filter(price__lte=max_price)

    # Sorting
    if sort_by == 'name_asc':
        services = services.order_by('name')
    elif sort_by == 'name_desc':
        services = services.order_by('-name')
    elif sort_by == 'price_low':
        services = services.order_by('price')
    elif sort_by == 'price_high':
        services = services.order_by('-price')
    else:
        services = services.order_by('-created_at')

    categories = Service.SERVICE_CATEGORIES

    context = {
        'services': services,
        'search_query': search_query,
        'selected_category': category,
        'selected_min_price': min_price,
        'selected_max_price': max_price,
        'selected_sort': sort_by,
        'categories': categories,
    }
    return render(request, 'services/service_list.html', context)


def service_detail(request, pk):
    service = get_object_or_404(Service, pk=pk)
    context = {'service': service}
    return render(request, 'services/service_detail.html', context)


@login_required
def service_create(request):
    if request.user.profile.role != 'shelter':
        messages.error(request, 'Only shelters can create service listings.')
        return redirect('service_list')

    if request.method == 'POST':
        form = ServiceForm(request.POST, request.FILES)
        if form.is_valid():
            service = form.save(commit=False)
            service.shelter = request.user
            service.save()
            messages.success(request, f'Service "{service.name}" has been listed successfully!')
            return redirect('service_detail', pk=service.pk)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ServiceForm()

    return render(request, 'services/service_form.html', {'form': form, 'title': 'Add New Service'})


@login_required
def service_update(request, pk):
    service = get_object_or_404(Service, pk=pk)

    if service.shelter != request.user:
        messages.error(request, 'You can only edit your own service listings.')
        return redirect('service_detail', pk=service.pk)

    if request.method == 'POST':
        form = ServiceForm(request.POST, request.FILES, instance=service)
        if form.is_valid():
            form.save()
            messages.success(request, f'Service "{service.name}" has been updated successfully!')
            return redirect('service_detail', pk=service.pk)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ServiceForm(instance=service)

    return render(request, 'services/service_form.html', {'form': form, 'title': 'Edit Service', 'service': service})


@login_required
def service_delete(request, pk):
    service = get_object_or_404(Service, pk=pk)

    if service.shelter != request.user:
        messages.error(request, 'You can only delete your own service listings.')
        return redirect('service_detail', pk=service.pk)

    if request.method == 'POST':
        service_name = service.name
        service.delete()
        messages.success(request, f'Service "{service_name}" has been deleted successfully!')
        return redirect('service_list')

    return render(request, 'services/service_confirm_delete.html', {'service': service})


@login_required
def my_services(request):
    if request.user.profile.role != 'shelter':
        messages.error(request, 'Only shelters can manage service listings.')
        return redirect('dashboard')

    services = Service.objects.filter(shelter=request.user).order_by('-created_at')
    return render(request, 'services/my_services.html', {'services': services})


# ==========================
# 📅 Booking Views (Updated)
# ==========================
@login_required
def booking_create(request, service_id):
    service = get_object_or_404(Service, pk=service_id, is_available=True)

    if request.user.profile.role != 'adopter':
        messages.error(request, 'Only adopters can book services.')
        return redirect('service_detail', pk=service_id)

    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.adopter = request.user
            booking.service = service
            booking.address = request.user.profile.address
            booking.save()

            # ✅ Notification for shelter
            create_booking_request_notification(booking)

            messages.success(request, f'Booking for {service.name} submitted successfully!')
            return redirect('my_bookings')
    else:
        form = BookingForm()

    return render(request, 'services/booking_form.html', {'form': form, 'service': service})


@login_required
def my_bookings(request):
    if request.user.profile.role != 'adopter':
        messages.error(request, 'Only adopters can view bookings.')
        return redirect('dashboard')

    bookings = Booking.objects.filter(adopter=request.user).select_related('service', 'service__shelter')
    return render(request, 'services/my_bookings.html', {'bookings': bookings})


@login_required
def booking_cancel(request, booking_id):
    booking = get_object_or_404(Booking, pk=booking_id, adopter=request.user)

    if not booking.can_be_cancelled():
        messages.error(request, 'This booking cannot be cancelled.')
        return redirect('my_bookings')

    if request.method == 'POST':
        booking.status = 'cancelled'
        booking.save()
        messages.success(request, f'Booking for {booking.service.name} has been cancelled.')
        return redirect('my_bookings')

    return render(request, 'services/booking_cancel.html', {'booking': booking})


@login_required
def shelter_bookings(request):
    if request.user.profile.role != 'shelter':
        messages.error(request, 'Only shelters can manage bookings.')
        return redirect('dashboard')

    bookings = Booking.objects.filter(
        service__shelter=request.user
    ).select_related('adopter', 'service').order_by('-created_at')

    status_filter = request.GET.get('status', '')
    if status_filter:
        bookings = bookings.filter(status=status_filter)

    return render(request, 'services/shelter_bookings.html', {'bookings': bookings, 'status_filter': status_filter})


@login_required
def booking_confirm(request, booking_id):
    booking = get_object_or_404(Booking, pk=booking_id, service__shelter=request.user)

    if booking.status != 'pending':
        messages.error(request, 'This booking cannot be confirmed.')
        return redirect('shelter_bookings')

    if request.method == 'POST':
        booking.status = 'confirmed'
        booking.save()

        # ✅ Notification to adopter
        create_booking_confirmed_notification(booking)

        messages.success(request, f'Booking for {booking.service.name} has been confirmed!')
        return redirect('shelter_bookings')

    return render(request, 'services/booking_confirm.html', {'booking': booking})


@login_required
def booking_start(request, booking_id):
    booking = get_object_or_404(Booking, pk=booking_id, service__shelter=request.user)

    if booking.status != 'confirmed':
        messages.error(request, 'This booking cannot be started.')
        return redirect('shelter_bookings')

    if request.method == 'POST':
        booking.status = 'in_progress'
        booking.save()

        # ✅ Notification to adopter
        create_booking_started_notification(booking)

        messages.success(request, f'Service {booking.service.name} has been started!')
        return redirect('shelter_bookings')

    return render(request, 'services/booking_start.html', {'booking': booking})


@login_required
def booking_complete(request, booking_id):
    booking = get_object_or_404(Booking, pk=booking_id, service__shelter=request.user)

    if booking.status != 'in_progress':
        messages.error(request, 'This booking cannot be completed.')
        return redirect('shelter_bookings')

    if request.method == 'POST':
        booking.status = 'completed'
        booking.save()

        # ✅ Notification to adopter
        create_booking_completed_notification(booking)

        messages.success(request, f'Service {booking.service.name} has been completed!')
        return redirect('shelter_bookings')

    return render(request, 'services/booking_complete.html', {'booking': booking})
