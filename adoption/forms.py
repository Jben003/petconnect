from django import forms
from django.utils import timezone
from .models import Pet, AdoptionRequest

class PetForm(forms.ModelForm):
    class Meta:
        model = Pet
        fields = ['name', 'pet_type', 'breed', 'age', 'gender', 'size', 'description', 'image', 'price']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter pet name'}),
            'pet_type': forms.Select(attrs={'class': 'form-control'}),
            'breed': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter breed'}),
            'age': forms.NumberInput(attrs={'class': 'form-control', 'min': '1', 'placeholder': 'Age in months'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'size': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Describe the pet\'s personality, habits, etc.'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0', 'placeholder': 'Adoption fee'}),
        }
        help_texts = {
            'age': 'Enter age in months (e.g., 6 for 6 months, 24 for 2 years)',
            'price': 'Set to 0 for free adoption',
        }

class AdoptionRequestForm(forms.ModelForm):
    class Meta:
        model = AdoptionRequest
        fields = ['message']
        widgets = {
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Tell us why you would be a great owner for this pet...'
            }),
        }
        help_texts = {
            'message': 'Share information about your experience with pets, your home environment, and why you want to adopt this pet.',
        }

class DeliveryStartForm(forms.ModelForm):
    estimated_delivery_date = forms.DateField(
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date',
            'min': timezone.now().date().isoformat()
        }),
        required=True,
        help_text="Select when you expect to deliver the pet"
    )
    
    class Meta:
        model = AdoptionRequest
        fields = ['estimated_delivery_date']
    
    def clean_estimated_delivery_date(self):
        delivery_date = self.cleaned_data['estimated_delivery_date']
        if delivery_date < timezone.now().date():
            raise forms.ValidationError('Estimated delivery date cannot be in the past.')
        return delivery_date

class DeliveryCompleteForm(forms.ModelForm):
    actual_delivery_date = forms.DateField(
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date',
            'max': timezone.now().date().isoformat()
        }),
        required=True
    )
    delivery_notes = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Add any delivery notes or special instructions...'
        }),
        required=False
    )
    
    class Meta:
        model = AdoptionRequest
        fields = ['actual_delivery_date', 'delivery_notes']

class RazorpayPaymentForm(forms.Form):
    """Form for Razorpay payment (no manual card input needed)"""
    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Your Name'
        }),
        required=True
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'your@email.com'
        }),
        required=True
    )
    phone = forms.CharField(
        max_length=15,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Phone Number'
        }),
        required=True
    )