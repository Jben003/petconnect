from django.shortcuts import render
from adoption.models import Pet

def home(request):
    # Get 3 random available pets for featured section
    featured_pets = Pet.objects.filter(is_available=True).order_by('?')[:3]
    
    context = {
        'featured_pets': featured_pets
    }
    return render(request, 'home.html', context)