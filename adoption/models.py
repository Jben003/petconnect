from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Pet(models.Model):
    PET_TYPES = (
        ('dog', 'Dog'),
        ('cat', 'Cat'),
        ('bird', 'Bird'),
        ('rabbit', 'Rabbit'),
        ('fish', 'Fish'),
        ('other', 'Other'),
    )
    
    GENDER_CHOICES = (
        ('male', 'Male'),
        ('female', 'Female'),
    )
    
    SIZE_CHOICES = (
        ('small', 'Small'),
        ('medium', 'Medium'),
        ('large', 'Large'),
    )
    
    name = models.CharField(max_length=100)
    pet_type = models.CharField(max_length=20, choices=PET_TYPES, default='dog')
    breed = models.CharField(max_length=100)
    age = models.PositiveIntegerField(help_text="Age in months")
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    size = models.CharField(max_length=10, choices=SIZE_CHOICES)
    description = models.TextField(max_length=1000)
    image = models.ImageField(upload_to='pet_images/', default='pet_images/default_pet.jpg')
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, help_text="Adoption fee")
    is_available = models.BooleanField(default=True)
    shelter = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'profile__role': 'shelter'})
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name} - {self.get_pet_type_display()}"
    
    def get_absolute_url(self):
        return reverse('pet_detail', kwargs={'pk': self.pk})
    
    @property
    def age_in_years(self):
        return self.age // 12
    
    @property
    def age_in_months(self):
        return self.age % 12
    
    def get_age_display(self):
        years = self.age_in_years
        months = self.age_in_months
        if years == 0:
            return f"{months} month{'s' if months != 1 else ''}"
        elif months == 0:
            return f"{years} year{'s' if years != 1 else ''}"
        else:
            return f"{years} year{'s' if years != 1 else ''} and {months} month{'s' if months != 1 else ''}"


class AdoptionRequest(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('in_delivery', 'In Delivery'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    )
    
    PAYMENT_STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    )
    
    adopter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='adoption_requests')
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, related_name='adoption_requests')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    delivery_address = models.TextField(max_length=500)
    message = models.TextField(max_length=1000, blank=True, help_text="Why do you want to adopt this pet?")
    
    # Delivery tracking fields
    estimated_delivery_date = models.DateField(null=True, blank=True)
    actual_delivery_date = models.DateField(null=True, blank=True)
    delivery_notes = models.TextField(max_length=500, blank=True)
    
    # Payment fields
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='pending')
    payment_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    payment_date = models.DateTimeField(null=True, blank=True)
    payment_reference = models.CharField(max_length=100, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['adopter', 'pet']  # Prevent duplicate requests
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.adopter.username} - {self.pet.name} ({self.status})"
    
    def save(self, *args, **kwargs):
        # Auto-set payment amount to pet's price when creating
        if not self.pk and self.pet:
            self.payment_amount = self.pet.price
        super().save(*args, **kwargs)
    
    def can_be_cancelled(self):
        return self.status in ['pending', 'approved']
    
    def can_be_approved(self):
        return self.status == 'pending'
    
    def can_be_rejected(self):
        return self.status == 'pending'
    
    def can_mark_in_delivery(self):
        return self.status == 'approved' and self.payment_status == 'completed'
    
    def can_mark_completed(self):
        return self.status == 'in_delivery'
    
    def can_process_payment(self):
        return self.status == 'approved' and self.payment_status == 'pending'
    
    def get_status_badge_class(self):
        status_classes = {
            'pending': 'bg-warning',
            'approved': 'bg-success',
            'rejected': 'bg-danger',
            'in_delivery': 'bg-info',
            'completed': 'bg-primary',
            'cancelled': 'bg-secondary',
        }
        return status_classes.get(self.status, 'bg-secondary')
    
    def get_payment_status_badge_class(self):
        status_classes = {
            'pending': 'bg-warning',
            'processing': 'bg-info',
            'completed': 'bg-success',
            'failed': 'bg-danger',
            'refunded': 'bg-secondary',
        }
        return status_classes.get(self.payment_status, 'bg-secondary')

class Notification(models.Model):
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='adoption_notifications'  # This makes it unique
    )
    message = models.TextField(max_length=500)
    related_url = models.CharField(max_length=200, blank=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.message[:50]}"
    
    def mark_as_read(self):
        self.is_read = True
        self.save()