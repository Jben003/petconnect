from django.urls import path
from . import views

urlpatterns = [
    path('', views.pet_list, name='pet_list'),
    path('pet/<int:pk>/', views.pet_detail, name='pet_detail'),
    path('pet/new/', views.pet_create, name='pet_create'),
    path('pet/<int:pk>/edit/', views.pet_update, name='pet_update'),
    path('pet/<int:pk>/delete/', views.pet_delete, name='pet_delete'),
    path('my-pets/', views.my_pets, name='my_pets'),
    
    # Adoption Request URLs - FIXED: using pet_id consistently
    path('pet/<int:pet_id>/adopt/', views.adoption_request_create, name='adoption_request_create'),
    path('my-requests/', views.my_adoption_requests, name='my_adoption_requests'),
    path('request/<int:request_id>/cancel/', views.adoption_request_cancel, name='adoption_request_cancel'),
    path('shelter/requests/', views.shelter_adoption_requests, name='shelter_adoption_requests'),
    path('request/<int:request_id>/approve/', views.adoption_request_approve, name='adoption_request_approve'),
    path('request/<int:request_id>/reject/', views.adoption_request_reject, name='adoption_request_reject'),
    
    # Delivery Management URLs
    path('request/<int:request_id>/start-delivery/', views.adoption_request_start_delivery, name='adoption_request_start_delivery'),
    path('request/<int:request_id>/complete-delivery/', views.adoption_request_complete_delivery, name='adoption_request_complete_delivery'),
    
    # Payment URLs
    path('request/<int:request_id>/payment/', views.process_payment, name='process_payment'),
    path('payment/success/', views.payment_success, name='payment_success'),
    path('payment/failed/', views.payment_failed, name='payment_failed'),
    path('request/<int:request_id>/payment/success/', views.payment_success_page, name='payment_success_page'),
    
    # Notification URLs
    path('notifications/', views.notification_list, name='notification_list'),
    path('notifications/<int:notification_id>/read/', views.mark_notification_read, name='mark_notification_read'),
    path('notifications/mark-all-read/', views.mark_all_notifications_read, name='mark_all_notifications_read'),
]