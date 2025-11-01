from django.contrib.auth.models import User
from .models import Notification

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