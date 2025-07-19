from django.contrib import admin
from .models import Vehicles, User, CustomerBookedVehicles, WishlistItem


# Custom filter for price range
class PriceFilter(admin.SimpleListFilter):
    title = 'Price Range'
    parameter_name = 'price_range'

    def lookups(self, request, model_admin):
        return (
            ('cheap', 'Cheap (< $1000)'),
            ('mid', 'Mid-range ($1000 - $5000)'),
            ('expensive', 'Expensive (> $5000)'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'cheap':
            return queryset.filter(price__lt=1000)
        if self.value() == 'mid':
            return queryset.filter(price__gte=1000, price__lte=5000)
        if self.value() == 'expensive':
            return queryset.filter(price__gt=5000)
        return queryset

class VehicleAdmin(admin.ModelAdmin):
        list_display = ('name', 'owner', 'price')  # Display owner in the list
        list_filter = (PriceFilter, 'owner')  # Filter by price and owner
        search_fields = ('name', 'description')  # Search by vehicle name or description

        fieldsets = (
            (None, {
                'fields': ('name', 'owner','image', 'price', 'description') # Now you can set owner in admin
            }),
        )
admin.site.register(Vehicles, VehicleAdmin) # Connect your admin class with your Vehicle model

class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_customer', 'is_owner', 'is_staff', 'is_active')  # Customize displayed fields
    list_filter = ('is_customer', 'is_owner', 'is_staff', 'is_active')  # Add filter for key user properties
    search_fields = ('username', 'email', 'first_name', 'last_name')  # Search by username, email, or names
    fieldsets = (
        (None, {
            'fields': ('username', 'password', 'email')  # Simplifies the form for the user
        }),
        ('Personal Info', {
            'fields': ('first_name', 'last_name')  # Allows setting first and last name
        }),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions', 'is_owner', 'is_customer')  # Key permissions
        }),
        ('Important dates', {
            'fields': ('last_login', 'date_joined')  # Information about user activity and timestamps
        }),
    )
admin.site.register(User,UserAdmin)

@admin.register(CustomerBookedVehicles)
class CustomerBookedVehiclesAdmin(admin.ModelAdmin):
    list_display = ('customer', 'vehicle', 'booking_date', 'pickup_location', 'dropoff_location', 'total_price') # What is shown in the list view
    list_filter = ('booking_date', 'customer', 'vehicle') # What is shown in the filter
    search_fields = ('customer__username', 'vehicle__name', 'pickup_location', 'dropoff_location')
     # Search is performed on the listed fields

@admin.register(WishlistItem)
class WishlistItemAdmin(admin.ModelAdmin):
    list_display = ('user', 'vehicle')
    search_fields = ('user__username', 'vehicle__name')