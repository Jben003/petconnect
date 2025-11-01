from django.urls import path
from . import views

urlpatterns = [
    path('', views.service_list, name='service_list'),
    path('service/<int:pk>/', views.service_detail, name='service_detail'),
    path('service/new/', views.service_create, name='service_create'),
    path('service/<int:pk>/edit/', views.service_update, name='service_update'),
    path('service/<int:pk>/delete/', views.service_delete, name='service_delete'),
    path('my-services/', views.my_services, name='my_services'),
    
    # Booking URLs
    path('service/<int:service_id>/book/', views.booking_create, name='booking_create'),
    path('my-bookings/', views.my_bookings, name='my_bookings'),
    path('booking/<int:booking_id>/cancel/', views.booking_cancel, name='booking_cancel'),
    path('shelter/bookings/', views.shelter_bookings, name='shelter_bookings'),
    path('booking/<int:booking_id>/confirm/', views.booking_confirm, name='booking_confirm'),
    path('booking/<int:booking_id>/start/', views.booking_start, name='booking_start'),
    path('booking/<int:booking_id>/complete/', views.booking_complete, name='booking_complete'),
]