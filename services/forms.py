from django import forms
from .models import Service, Booking
from django.utils import timezone

class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['name', 'description', 'price', 'category', 'image', 'duration']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter service name'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Describe the service...'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0', 'placeholder': 'Service price'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'duration': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., 1 hour, 30 minutes'}),
        }
        help_texts = {
            'duration': 'Enter the duration of the service (e.g., 1 hour, 30 minutes)',
        }

class BookingForm(forms.ModelForm):
    booking_date = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={
            'class': 'form-control',
            'type': 'datetime-local',
            'min': timezone.now().strftime('%Y-%m-%dT%H:%M')
        }),
        required=True
    )
    
    class Meta:
        model = Booking
        fields = ['booking_date', 'special_instructions']
        widgets = {
            'special_instructions': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Any special instructions or requirements...'
            }),
        }
    
    def clean_booking_date(self):
        booking_date = self.cleaned_data['booking_date']
        if booking_date < timezone.now():
            raise forms.ValidationError('Booking date cannot be in the past.')
        return booking_date