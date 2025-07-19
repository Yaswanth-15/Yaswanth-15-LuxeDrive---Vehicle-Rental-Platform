from django.urls import path
from . import views

urlpatterns = [
    # existing URLs
    path('', views.home, name='home'),
    path('vehicles/', views.vehicles, name='vehicles'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('booking/', views.booking, name='booking'),
    path('booking_confirmation/', views.booking_confirmation, name='booking_confirmation'),
    path('register/customer/', views.register_customer, name='register_customer'),
    path('register/owner/', views.register_owner, name='register_owner'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('booked_vehicles/', views.booked_vehicles, name='booked_vehicles'),
    path('my_vehicles/', views.my_vehicles, name='my_vehicles'),  # Owner's vehicle management page
    path('add_vehicle/', views.add_vehicle, name='add_vehicle'),
    path('edit_vehicle/<int:vehicle_id>/', views.edit_vehicle, name='edit_vehicle'),
    path('delete_vehicle/<int:vehicle_id>/', views.delete_vehicle, name='delete_vehicle'),
    path('owner_bookings/', views.owner_bookings, name='owner_bookings'),
    # ADD TO WISHLIST URLS
    path('add_to_wishlist/<int:vehicle_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('wishlist/', views.wishlist, name='wishlist'),
    path('remove_from_wishlist/<int:vehicle_id>/', views.remove_from_wishlist, name='remove_from_wishlist'), #THIS LINE IS IMPORTANT

]