from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate, get_user_model, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm, CustomPasswordChangeForm
from .models import Profile
from adoption.models import Pet, AdoptionRequest
from services.models import Service, Booking



def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            role = form.cleaned_data.get('role')
            messages.success(request, f'Account created for {username}! You are registered as a {role}. You can now log in.')
            return redirect('login')
        else:
            # Print form errors for debugging
            print("Form errors:", form.errors)
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = UserRegisterForm()
    
    return render(request, 'accounts/register.html', {'form': form})


def custom_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(f"Login attempt - Username: {username}")  # Debug
        
        # Try to authenticate with both username and email
        User = get_user_model()
        try:
            # First try with username
            user = authenticate(request, username=username, password=password)
            
            # If that fails, try with email
            if user is None:
                try:
                    user_obj = User.objects.get(email=username)
                    user = authenticate(request, username=user_obj.username, password=password)
                except User.DoesNotExist:
                    pass
            
            print(f"Authenticated user: {user}")  # Debug
            
            if user is not None:
                if user.is_active:
                    login(request, user)
                    messages.success(request, f'Welcome back, {user.username}!')
                    
                    # Redirect based on role
                    if hasattr(user, 'profile'):
                        if user.profile.role == 'shelter':
                            return redirect('shelter_dashboard')
                        else:
                            return redirect('adopter_dashboard')
                    return redirect('dashboard')
                else:
                    messages.error(request, 'Your account is disabled.')
            else:
                messages.error(request, 'Invalid username/email or password. Please try again.')
                
        except Exception as e:
            print(f"Login error: {e}")  # Debug
            messages.error(request, 'An error occurred during login. Please try again.')
    
    return render(request, 'accounts/login.html')


def custom_logout(request):
    logout(request)
    messages.info(request, 'You have been logged out successfully.')
    return redirect('home')


@login_required
def profile(request):
    # Check if user is admin (no profile needed)
    if request.user.is_superuser or request.user.is_staff:
        # Get platform statistics for admin
        total_users = User.objects.count()
        total_pets = Pet.objects.count()
        total_services = Service.objects.count()
        total_adoption_requests = AdoptionRequest.objects.count()
        
        if request.method == 'POST':
            u_form = UserUpdateForm(request.POST, instance=request.user)
            if u_form.is_valid():
                u_form.save()
                messages.success(request, 'Your account has been updated!')
                return redirect('profile')
        else:
            u_form = UserUpdateForm(instance=request.user)

        context = {
            'u_form': u_form,
            'is_admin': True,
            'total_users': total_users,
            'total_pets': total_pets,
            'total_services': total_services,
            'total_adoption_requests': total_adoption_requests,
        }
        return render(request, 'accounts/profile.html', context)
    
    # Regular users with profiles
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, instance=request.user.profile)
        
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form,
        'is_admin': False
    }
    return render(request, 'accounts/profile.html', context)


@login_required
def dashboard(request):
    user = request.user
    
    # Redirect admins to admin dashboard
    if user.is_superuser or user.is_staff:
        return redirect('admin_dashboard')
    
    # Check if user has profile
    if hasattr(user, 'profile'):
        profile = user.profile
        if profile.role == 'shelter':
            return redirect('shelter_dashboard')
        else:
            return redirect('adopter_dashboard')
    else:
        # If no profile, redirect to profile creation or home
        messages.warning(request, 'Please complete your profile setup.')
        return redirect('profile')


@login_required
def shelter_dashboard(request):
    if request.user.profile.role != 'shelter':
        messages.error(request, 'Access denied. Shelter account required.')
        return redirect('dashboard')
    
    context = {
        'shelter_pets': [],
        'adoption_requests': [],
    }
    return render(request, 'accounts/shelter_dashboard.html', context)


@login_required
def adopter_dashboard(request):
    if request.user.profile.role != 'adopter':
        messages.error(request, 'Access denied. Adopter account required.')
        return redirect('dashboard')
    
    context = {
        'my_adoption_requests': [],
        'my_bookings': [],
    }
    return render(request, 'accounts/adopter_dashboard.html', context)


@login_required
def admin_dashboard(request):
    """Admin dashboard for platform overview"""
    if not request.user.is_superuser and not request.user.is_staff:
        messages.error(request, 'Access denied. Admin privileges required.')
        return redirect('dashboard')
    
    # Platform statistics
    total_users = User.objects.count()
    total_pets = Pet.objects.count()
    total_services = Service.objects.count()
    total_adoption_requests = AdoptionRequest.objects.count()
    total_bookings = Booking.objects.count()
    
    # Recent activities
    recent_pets = Pet.objects.all().order_by('-created_at')[:5]
    recent_services = Service.objects.all().order_by('-created_at')[:5]
    recent_adoption_requests = AdoptionRequest.objects.all().select_related('pet', 'adopter').order_by('-created_at')[:5]
    
    # User statistics by role
    adopters_count = Profile.objects.filter(role='adopter').count()
    shelters_count = Profile.objects.filter(role='shelter').count()
    
    context = {
        'total_users': total_users,
        'total_pets': total_pets,
        'total_services': total_services,
        'total_adoption_requests': total_adoption_requests,
        'total_bookings': total_bookings,
        'adopters_count': adopters_count,
        'shelters_count': shelters_count,
        'recent_pets': recent_pets,
        'recent_services': recent_services,
        'recent_adoption_requests': recent_adoption_requests,
    }
    return render(request, 'accounts/admin_dashboard.html', context)
