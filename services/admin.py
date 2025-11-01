from django.contrib import admin
from .models import Service, Booking

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'duration', 'shelter', 'is_available', 'created_at']
    list_filter = ['category', 'is_available', 'created_at', 'shelter']
    search_fields = ['name', 'description', 'shelter__username']
    list_editable = ['is_available', 'price']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'created_at'

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['adopter', 'service', 'status', 'booking_date', 'created_at']
    list_filter = ['status', 'booking_date', 'created_at', 'service__category']
    search_fields = ['adopter__username', 'service__name', 'special_instructions']
    list_editable = ['status']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'created_at'