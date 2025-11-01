from django.db import models
from django.contrib.auth.models import User

class Service(models.Model):
    SERVICE_CATEGORIES = (
        ('grooming', 'Grooming'),
        ('veterinary', 'Veterinary Care'),
        ('training', 'Training'),
        ('boarding', 'Boarding'),
        ('walking', 'Dog Walking'),
        ('sitting', 'Pet Sitting'),
        ('other', 'Other'),
    )
    
    name = models.CharField(max_length=200)
    description = models.TextField(max_length=1000)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=20, choices=SERVICE_CATEGORIES, default='other')
    image = models.ImageField(upload_to='service_images/', default='service_images/default_service.jpg')
    duration = models.CharField(max_length=50, help_text="e.g., 1 hour, 30 minutes")
    shelter = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'profile__role': 'shelter'})
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name} - {self.shelter.username}"
    
    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('service_detail', kwargs={'pk': self.pk})

class Booking(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    )
    
    adopter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='service_bookings')
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='bookings')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    booking_date = models.DateTimeField()
    special_instructions = models.TextField(max_length=500, blank=True)
    address = models.TextField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.adopter.username} - {self.service.name}"
    
    def can_be_cancelled(self):
        return self.status in ['pending', 'confirmed']
    
    def get_status_badge_class(self):
        status_classes = {
            'pending': 'bg-warning',
            'confirmed': 'bg-success',
            'in_progress': 'bg-info',
            'completed': 'bg-primary',
            'cancelled': 'bg-secondary',
        }
        return status_classes.get(self.status, 'bg-secondary')