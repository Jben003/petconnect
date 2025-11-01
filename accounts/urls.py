from django.urls import path
from . import views

urlpatterns = [
    # Authentication & Profile
    path('register/', views.register, name='register'),
    path('login/', views.custom_login, name='login'),
    path('logout/', views.custom_logout, name='logout'),
    path('profile/', views.profile, name='profile'),

    # Dashboards
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/admin/', views.admin_dashboard, name='admin_dashboard'),
    path('dashboard/shelter/', views.shelter_dashboard, name='shelter_dashboard'),
    path('dashboard/adopter/', views.adopter_dashboard, name='adopter_dashboard'),

]
