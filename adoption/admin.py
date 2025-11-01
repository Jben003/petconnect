from django.contrib import admin
from .models import Pet, AdoptionRequest, Notification

@admin.register(Pet)
class PetAdmin(admin.ModelAdmin):
    list_display = ['name', 'pet_type', 'breed', 'age', 'gender', 'is_available', 'shelter', 'created_at']
    list_filter = ['pet_type', 'gender', 'size', 'is_available', 'created_at']
    search_fields = ['name', 'breed', 'description', 'shelter__username']
    list_editable = ['is_available']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'pet_type', 'breed', 'age', 'gender', 'size')
        }),
        ('Details', {
            'fields': ('description', 'image', 'price', 'is_available')
        }),
        ('Shelter Information', {
            'fields': ('shelter',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(AdoptionRequest)
class AdoptionRequestAdmin(admin.ModelAdmin):
    list_display = ['adopter', 'pet', 'status', 'payment_status', 'created_at', 'updated_at']
    list_filter = ['status', 'payment_status', 'created_at', 'pet__pet_type']
    search_fields = ['adopter__username', 'pet__name', 'message']
    list_editable = ['status', 'payment_status']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Request Information', {
            'fields': ('adopter', 'pet', 'status', 'delivery_address', 'message')
        }),
        ('Payment Information', {
            'fields': ('payment_status', 'payment_amount', 'payment_date', 'payment_reference')
        }),
        ('Delivery Information', {
            'fields': ('estimated_delivery_date', 'actual_delivery_date', 'delivery_notes')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['user', 'message', 'is_read', 'created_at']
    list_filter = ['is_read', 'created_at']
    search_fields = ['user__username', 'message']
    list_editable = ['is_read']
    readonly_fields = ['created_at']
    
    fieldsets = (
        ('Notification Information', {
            'fields': ('user', 'message', 'related_url', 'is_read')
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )