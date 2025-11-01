from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Count
from django.utils import timezone
from django.http import JsonResponse
from django.db import IntegrityError
from datetime import timedelta
import random
import string
import time


from django.conf import settings
from .models import Pet, AdoptionRequest, Notification
from .forms import (
    PetForm,
    AdoptionRequestForm,
    DeliveryStartForm,
    DeliveryCompleteForm, 
    RazorpayPaymentForm,
)
from .razorpay_utils import create_razorpay_order, verify_razorpay_payment, get_razorpay_payment_details



# Utility functions
def update_payment_status(adoption_request):
    """Auto-complete payment for free adoptions"""
    if adoption_request.payment_amount == 0:
        adoption_request.payment_status = 'completed'
        adoption_request.payment_date = timezone.now()
        adoption_request.payment_reference = 'FREE-ADOPTION'
        adoption_request.save()
        return True
    return False



def create_notification(user, message, related_url=''):
    """Create a new notification for a user"""
    notification = Notification.objects.create(
        user=user,
        message=message,
        related_url=related_url
    )
    return notification



def create_adoption_request_notification(adoption_request):
    """Create notification for shelter when adoption request is made"""
    message = f"New adoption request for {adoption_request.pet.name} from {adoption_request.adopter.username}"
    related_url = f"/adoption/shelter/requests/"
    create_notification(adoption_request.pet.shelter, message, related_url)



def create_adoption_approved_notification(adoption_request):
    """Create notification for adopter when adoption is approved"""
    message = f"Your adoption request for {adoption_request.pet.name} has been approved!"
    related_url = f"/adoption/my-requests/"
    create_notification(adoption_request.adopter, message, related_url)



def create_adoption_rejected_notification(adoption_request):
    """Create notification for adopter when adoption is rejected"""
    message = f"Your adoption request for {adoption_request.pet.name} has been rejected."
    related_url = f"/adoption/my-requests/"
    create_notification(adoption_request.adopter, message, related_url)



def create_payment_completed_notification(adoption_request):
    """Create notification for shelter when payment is completed"""
    message = f"Payment received for {adoption_request.pet.name} from {adoption_request.adopter.username}"
    related_url = f"/adoption/shelter/requests/"
    create_notification(adoption_request.pet.shelter, message, related_url)



def create_delivery_started_notification(adoption_request):
    """Create notification for adopter when delivery starts"""
    message = f"Delivery started for {adoption_request.pet.name}! Estimated delivery: {adoption_request.estimated_delivery_date}"
    related_url = f"/adoption/my-requests/"
    create_notification(adoption_request.adopter, message, related_url)



def create_delivery_completed_notification(adoption_request):
    """Create notification for adopter when delivery is completed"""
    message = f"Delivery completed for {adoption_request.pet.name}! Welcome your new pet home!"
    related_url = f"/adoption/my-requests/"
    create_notification(adoption_request.adopter, message, related_url)



def get_unread_notifications_count(user):
    """Get count of unread notifications for a user"""
    return Notification.objects.filter(user=user, is_read=False).count()



def get_recent_notifications(user, limit=5):
    """Get recent notifications for a user"""
    return Notification.objects.filter(user=user).order_by('-created_at')[:limit]



# Booking notification functions
def create_booking_notification(booking, message, notification_type='info'):
    """Create notification for booking activities"""
    if notification_type == 'info':
        create_notification(booking.service.shelter, message, '/services/shelter/bookings/')
    elif notification_type == 'success':
        create_notification(booking.adopter, message, '/services/my-bookings/')



def create_booking_request_notification(booking):
    """Create notification for shelter when booking is made"""
    message = f"New booking for {booking.service.name} from {booking.adopter.username}"
    create_booking_notification(booking, message, 'info')



def create_booking_confirmed_notification(booking):
    """Create notification for adopter when booking is confirmed"""
    message = f"Your booking for {booking.service.name} has been confirmed!"
    create_booking_notification(booking, message, 'success')



def create_booking_started_notification(booking):
    """Create notification for adopter when service starts"""
    message = f"Service {booking.service.name} has started!"
    create_booking_notification(booking, message, 'info')



def create_booking_completed_notification(booking):
    """Create notification for adopter when service completes"""
    message = f"Service {booking.service.name} has been completed!"
    create_booking_notification(booking, message, 'success')



# Main views
def pet_list(request):
    pets = Pet.objects.filter(is_available=True).order_by('-created_at')
    
    # Get filter parameters
    search_query = request.GET.get('search', '')
    pet_type = request.GET.get('type', '')
    gender = request.GET.get('gender', '')
    size = request.GET.get('size', '')
    min_age = request.GET.get('min_age', '')
    max_age = request.GET.get('max_age', '')
    min_price = request.GET.get('min_price', '')
    max_price = request.GET.get('max_price', '')
    sort_by = request.GET.get('sort_by', 'newest')
    
    # Search functionality
    if search_query:
        pets = pets.filter(
            Q(name__icontains=search_query) | 
            Q(breed__icontains=search_query) |
            Q(description__icontains=search_query)
        )
    
    if pet_type:
        pets = pets.filter(pet_type=pet_type)
    if gender:
        pets = pets.filter(gender=gender)
    if size:
        pets = pets.filter(size=size)
    if min_age:
        pets = pets.filter(age__gte=min_age)
    if max_age:
        pets = pets.filter(age__lte=max_age)
    if min_price:
        pets = pets.filter(price__gte=min_price)
    if max_price:
        pets = pets.filter(price__lte=max_price)
    
    # Sorting
    if sort_by == 'name_asc':
        pets = pets.order_by('name')
    elif sort_by == 'name_desc':
        pets = pets.order_by('-name')
    elif sort_by == 'price_low':
        pets = pets.order_by('price')
    elif sort_by == 'price_high':
        pets = pets.order_by('-price')
    elif sort_by == 'age_low':
        pets = pets.order_by('age')
    elif sort_by == 'age_high':
        pets = pets.order_by('-age')
    else:
        pets = pets.order_by('-created_at')
    
    pet_types_count = pets.values('pet_type').distinct().count()
    shelters_count = pets.values('shelter').distinct().count()
    
    pet_types = Pet.PET_TYPES
    gender_choices = Pet.GENDER_CHOICES
    size_choices = Pet.SIZE_CHOICES
    
    context = {
        'pets': pets,
        'search_query': search_query,
        'selected_type': pet_type,
        'selected_gender': gender,
        'selected_size': size,
        'selected_min_age': min_age,
        'selected_max_age': max_age,
        'selected_min_price': min_price,
        'selected_max_price': max_price,
        'selected_sort': sort_by,
        'pet_types': pet_types,
        'gender_choices': gender_choices,
        'size_choices': size_choices,
        'pet_types_count': pet_types_count,
        'shelters_count': shelters_count,
    }
    return render(request, 'adoption/pet_list.html', context)



def pet_detail(request, pk):
    pet = get_object_or_404(Pet, pk=pk)
    return render(request, 'adoption/pet_detail.html', {'pet': pet})



@login_required
def pet_create(request):
    if request.user.profile.role != 'shelter':
        messages.error(request, 'Only shelters can create pet listings.')
        return redirect('pet_list')
    
    if request.method == 'POST':
        form = PetForm(request.POST, request.FILES)
        if form.is_valid():
            pet = form.save(commit=False)
            pet.shelter = request.user
            pet.save()
            messages.success(request, f'Pet "{pet.name}" has been listed successfully!')
            return redirect('pet_detail', pk=pet.pk)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = PetForm()
    
    return render(request, 'adoption/pet_form.html', {'form': form, 'title': 'Add New Pet'})



@login_required
def pet_update(request, pk):
    pet = get_object_or_404(Pet, pk=pk)
    if pet.shelter != request.user:
        messages.error(request, 'You can only edit your own pet listings.')
        return redirect('pet_detail', pk=pet.pk)
    
    if request.method == 'POST':
        form = PetForm(request.POST, request.FILES, instance=pet)
        if form.is_valid():
            form.save()
            messages.success(request, f'Pet "{pet.name}" has been updated successfully!')
            return redirect('pet_detail', pk=pet.pk)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = PetForm(instance=pet)
    
    return render(request, 'adoption/pet_form.html', {'form': form, 'title': 'Edit Pet', 'pet': pet})



@login_required
def pet_delete(request, pk):
    pet = get_object_or_404(Pet, pk=pk)
    if pet.shelter != request.user:
        messages.error(request, 'You can only delete your own pet listings.')
        return redirect('pet_detail', pk=pet.pk)
    
    if request.method == 'POST':
        pet_name = pet.name
        pet.delete()
        messages.success(request, f'Pet "{pet_name}" has been deleted successfully!')
        return redirect('pet_list')
    
    return render(request, 'adoption/pet_confirm_delete.html', {'pet': pet})



@login_required
def my_pets(request):
    if request.user.profile.role != 'shelter':
        messages.error(request, 'Only shelters can manage pet listings.')
        return redirect('dashboard')
    
    pets = Pet.objects.filter(shelter=request.user).order_by('-created_at')
    return render(request, 'adoption/my_pets.html', {'pets': pets})



@login_required
def adoption_request_create(request, pet_id):
    pet = get_object_or_404(Pet, pk=pet_id, is_available=True)
    
    if request.user.profile.role != 'adopter':
        messages.error(request, 'Only adopters can submit adoption requests.')
        return redirect('pet_detail', pk=pet_id)
    
    existing_request = AdoptionRequest.objects.filter(adopter=request.user, pet=pet).first()
    if existing_request:
        status_display = existing_request.get_status_display().lower()
        messages.warning(request, f'You already have a {status_display} adoption request for {pet.name}.')
        return redirect('pet_detail', pk=pet_id)
    
    if request.method == 'POST':
        print("POST request received")
        form = AdoptionRequestForm(request.POST)
        print(f"Form is valid: {form.is_valid()}")
        print(f"Form data: {request.POST}")
        
        if form.is_valid():
            try:
                adoption_request = form.save(commit=False)
                adoption_request.adopter = request.user
                adoption_request.pet = pet
                adoption_request.delivery_address = request.user.profile.address
                adoption_request.save()
                print("Adoption request saved successfully")
                
                create_adoption_request_notification(adoption_request)
                messages.success(request, f'Adoption request for {pet.name} submitted successfully!')
                return redirect('my_adoption_requests')
                
            except IntegrityError as e:
                print(f"IntegrityError: {e}")
                messages.error(request, 'You have already submitted an adoption request for this pet.')
                return redirect('pet_detail', pk=pet_id)
            except Exception as e:
                print(f"Unexpected error: {e}")
                messages.error(request, 'An unexpected error occurred. Please try again.')
                return redirect('pet_detail', pk=pet_id)
        else:
            print(f"Form errors: {form.errors}")
            messages.error(request, 'Please correct the errors below.')
    else:
        form = AdoptionRequestForm()
    
    return render(request, 'adoption/adoption_request_form.html', {'form': form, 'pet': pet})



@login_required
def my_adoption_requests(request):
    if request.user.profile.role != 'adopter':
        messages.error(request, 'Only adopters can view adoption requests.')
        return redirect('dashboard')
    
    adoption_requests = AdoptionRequest.objects.filter(adopter=request.user).select_related('pet', 'pet__shelter')
    return render(request, 'adoption/my_adoption_requests.html', {'adoption_requests': adoption_requests})



@login_required
def adoption_request_cancel(request, request_id):
    adoption_request = get_object_or_404(AdoptionRequest, pk=request_id, adopter=request.user)
    if not adoption_request.can_be_cancelled():
        messages.error(request, 'This adoption request cannot be cancelled.')
        return redirect('my_adoption_requests')
    
    if request.method == 'POST':
        adoption_request.status = 'cancelled'
        adoption_request.save()
        messages.success(request, f'Adoption request for {adoption_request.pet.name} has been cancelled.')
        return redirect('my_adoption_requests')
    
    return render(request, 'adoption/adoption_request_cancel.html', {'adoption_request': adoption_request})



@login_required
def shelter_adoption_requests(request):
    if request.user.profile.role != 'shelter':
        messages.error(request, 'Only shelters can manage adoption requests.')
        return redirect('dashboard')
    
    adoption_requests = AdoptionRequest.objects.filter(
        pet__shelter=request.user
    ).select_related('adopter', 'pet').order_by('-created_at')
    
    status_filter = request.GET.get('status', '')
    if status_filter:
        adoption_requests = adoption_requests.filter(status=status_filter)
    
    return render(request, 'adoption/shelter_adoption_requests.html', {
        'adoption_requests': adoption_requests,
        'status_filter': status_filter
    })



@login_required
def adoption_request_approve(request, request_id):
    adoption_request = get_object_or_404(AdoptionRequest, pk=request_id, pet__shelter=request.user)
    if not adoption_request.can_be_approved():
        messages.error(request, 'This adoption request cannot be approved.')
        return redirect('shelter_adoption_requests')
    
    if request.method == 'POST':
        AdoptionRequest.objects.filter(pet=adoption_request.pet, status='pending').exclude(pk=request_id).update(status='rejected')
        adoption_request.status = 'approved'
        adoption_request.save()
        
        if adoption_request.payment_amount == 0:
            update_payment_status(adoption_request)
            payment_msg = " (Payment auto-completed for free adoption)"
        else:
            payment_msg = " (Payment pending)"
        
        adoption_request.pet.is_available = False
        adoption_request.pet.save()
        create_adoption_approved_notification(adoption_request)
        
        messages.success(request, f'Adoption request for {adoption_request.pet.name} has been approved!{payment_msg}')
        return redirect('shelter_adoption_requests')
    
    return render(request, 'adoption/adoption_request_approve.html', {'adoption_request': adoption_request})



@login_required
def adoption_request_reject(request, request_id):
    adoption_request = get_object_or_404(AdoptionRequest, pk=request_id, pet__shelter=request.user)
    if not adoption_request.can_be_rejected():
        messages.error(request, 'This adoption request cannot be rejected.')
        return redirect('shelter_adoption_requests')
    
    if request.method == 'POST':
        adoption_request.status = 'rejected'
        adoption_request.save()
        create_adoption_rejected_notification(adoption_request)
        messages.success(request, f'Adoption request for {adoption_request.pet.name} has been rejected.')
        return redirect('shelter_adoption_requests')
    
    return render(request, 'adoption/adoption_request_reject.html', {'adoption_request': adoption_request})



@login_required
def adoption_request_start_delivery(request, request_id):
    adoption_request = get_object_or_404(AdoptionRequest, pk=request_id, pet__shelter=request.user)
    
    print(f"Delivery Start - Status: {adoption_request.status}, Payment Status: {adoption_request.payment_status}, Amount: {adoption_request.payment_amount}")
    
    if not adoption_request.can_mark_in_delivery():
        if adoption_request.status != 'approved':
            messages.error(request, f'Cannot start delivery. Request status is {adoption_request.get_status_display()}, but should be Approved.')
        elif adoption_request.payment_status != 'completed' and adoption_request.payment_amount > 0:
            messages.error(request, f'Cannot start delivery. Payment of ₹{adoption_request.payment_amount} is pending.')
        else:
            messages.error(request, 'This adoption request cannot be marked as in delivery.')
        return redirect('shelter_adoption_requests')
    
    if request.method == 'POST':
        form = DeliveryStartForm(request.POST, instance=adoption_request)
        if form.is_valid():
            adoption_request = form.save(commit=False)
            adoption_request.status = 'in_delivery'
            adoption_request.save()
            create_delivery_started_notification(adoption_request)
            messages.success(request, f'Delivery started for {adoption_request.pet.name}! Estimated delivery: {adoption_request.estimated_delivery_date}')
            return redirect('shelter_adoption_requests')
        else:
            messages.error(request, 'Please correct the errors in the form.')
    else:
        default_date = timezone.now().date() + timedelta(days=3)
        form = DeliveryStartForm(initial={'estimated_delivery_date': default_date})
    
    return render(request, 'adoption/adoption_request_start_delivery.html', {
        'form': form,
        'adoption_request': adoption_request
    })



@login_required
def adoption_request_complete_delivery(request, request_id):
    adoption_request = get_object_or_404(AdoptionRequest, pk=request_id, pet__shelter=request.user)
    if not adoption_request.can_mark_completed():
        messages.error(request, 'This adoption request cannot be marked as completed.')
        return redirect('shelter_adoption_requests')
    
    if request.method == 'POST':
        form = DeliveryCompleteForm(request.POST, instance=adoption_request)
        if form.is_valid():
            adoption_request = form.save(commit=False)
            adoption_request.status = 'completed'
            adoption_request.save()
            create_delivery_completed_notification(adoption_request)
            messages.success(request, f'Delivery completed for {adoption_request.pet.name}! The adoption process is now complete.')
            return redirect('shelter_adoption_requests')
    else:
        form = DeliveryCompleteForm(instance=adoption_request)
    
    return render(request, 'adoption/adoption_request_complete_delivery.html', {
        'form': form,
        'adoption_request': adoption_request
    })



@login_required
def process_payment(request, request_id):
    adoption_request = get_object_or_404(
        AdoptionRequest, 
        pk=request_id, 
        adopter=request.user
    )
    
    # Debug information
    print(f"Payment Process - Status: {adoption_request.status}, Payment Status: {adoption_request.payment_status}, Amount: {adoption_request.payment_amount}")
    
    if not adoption_request.can_process_payment():
        messages.error(request, 'Payment cannot be processed for this adoption request.')
        return redirect('my_adoption_requests')
    
    if request.method == 'POST':
        form = RazorpayPaymentForm(request.POST)
        if form.is_valid():
            razorpay_order = create_razorpay_order(adoption_request.payment_amount)
            if razorpay_order:
                request.session['razorpay_order_id'] = razorpay_order['id']
                request.session['adoption_request_id'] = adoption_request.pk
                request.session['payment_amount'] = str(adoption_request.payment_amount)
                
                return render(request, 'adoption/razorpay_payment.html', {
                    'adoption_request': adoption_request,
                    'razorpay_order': razorpay_order,
                    'razorpay_key_id': settings.RAZORPAY_KEY_ID,
                    'user': request.user,
                    'form_data': form.cleaned_data
                })
            else:
                messages.error(request, 'Failed to create payment order. Please try again.')
    else:
        initial_data = {
            'name': f"{request.user.first_name} {request.user.last_name}".strip() or request.user.username,
            'email': request.user.email,
            'phone': request.user.profile.phone_number
        }
        form = RazorpayPaymentForm(initial=initial_data)
    
    return render(request, 'adoption/process_payment.html', {
        'form': form,
        'adoption_request': adoption_request
    })



@login_required
def payment_success(request):
    if request.method == 'POST':
        try:
            razorpay_payment_id = request.POST.get('razorpay_payment_id')
            razorpay_order_id = request.POST.get('razorpay_order_id')
            razorpay_signature = request.POST.get('razorpay_signature')
            session_order_id = request.session.get('razorpay_order_id')
            adoption_request_id = request.session.get('adoption_request_id')
            
            if not all([razorpay_payment_id, razorpay_order_id, razorpay_signature, session_order_id, adoption_request_id]):
                messages.error(request, 'Invalid payment data.')
                return redirect('my_adoption_requests')
            
            if razorpay_order_id != session_order_id:
                messages.error(request, 'Order ID mismatch.')
                return redirect('my_adoption_requests')
            
            if verify_razorpay_payment(razorpay_order_id, razorpay_payment_id, razorpay_signature):
                adoption_request = get_object_or_404(AdoptionRequest, pk=adoption_request_id, adopter=request.user)
                adoption_request.payment_status = 'completed'
                adoption_request.payment_date = timezone.now()
                adoption_request.payment_reference = razorpay_payment_id
                adoption_request.save()
                create_payment_completed_notification(adoption_request)
                
                for key in ['razorpay_order_id', 'adoption_request_id', 'payment_amount']:
                    request.session.pop(key, None)
                
                messages.success(request, f'Payment of ₹{adoption_request.payment_amount} completed successfully!')
                return redirect('payment_success_page', request_id=adoption_request.pk)
            else:
                messages.error(request, 'Payment verification failed.')
        except Exception as e:
            messages.error(request, f'Payment processing error: {str(e)}')
    else:
        messages.error(request, 'Invalid request method.')
    return redirect('my_adoption_requests')



@login_required
def payment_failed(request):
    adoption_request_id = request.session.get('adoption_request_id')
    if adoption_request_id:
        adoption_request = get_object_or_404(AdoptionRequest, pk=adoption_request_id, adopter=request.user)
        adoption_request.payment_status = 'failed'
        adoption_request.save()
    
    for key in ['razorpay_order_id', 'adoption_request_id', 'payment_amount']:
        request.session.pop(key, None)
    
    messages.error(request, 'Payment failed. Please try again.')
    return redirect('my_adoption_requests')



@login_required
def payment_success_page(request, request_id):
    adoption_request = get_object_or_404(AdoptionRequest, pk=request_id, adopter=request.user)
    return render(request, 'adoption/payment_success.html', {'adoption_request': adoption_request})



@login_required
def notification_list(request):
    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
    unread_count = notifications.filter(is_read=False).count()
    read_count = notifications.filter(is_read=True).count()
    today_count = notifications.filter(created_at__date=timezone.now().date()).count()
    
    notifications.filter(is_read=False).update(is_read=True)
    
    return render(request, 'adoption/notification_list.html', {
        'notifications': notifications,
        'unread_count': unread_count,
        'read_count': read_count,
        'today_count': today_count,
    })



@login_required
def mark_notification_read(request, notification_id):
    notification = get_object_or_404(Notification, pk=notification_id, user=request.user)
    notification.is_read = True
    notification.save()
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'success': True})
    return redirect('notification_list')



@login_required
def mark_all_notifications_read(request):
    Notification.objects.filter(user=request.user, is_read=False).update(is_read=True)
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'success': True})
    return redirect('notification_list')
