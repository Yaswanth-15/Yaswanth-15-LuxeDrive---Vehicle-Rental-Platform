from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import CustomerRegistrationForm, OwnerRegistrationForm, VehicleForm, CreateBookingsForm
from .models import Vehicles, CustomerBookedVehicles, User, WishlistItem #ADD TO WISHLIST
from website.utils.decimal_to_float import Decimal2Float
from datetime import date # Added for Date field
from decimal import Decimal
from django.db.models import Q
import json

# Pages
def home(request):
    vehicles = Vehicles.objects.all()
    return render(request, 'home.html',{'vehicles': vehicles})

# VEHICLES PAGE VIEW
def vehicles(request):
    query = request.GET.get('term', '') # Get the search term from AJAX request or URL parameter
    vehicles = Vehicles.objects.all()

    if query:
        vehicles = Vehicles.objects.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        ).distinct()

    if request.headers.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        # AJAX request - return suggestions
        suggestions = []
        for vehicle in vehicles:
            suggestions.append({
                'id': vehicle.id,
                'name': vehicle.name,
                #'url': reverse('booking') + f'?vehicle_id={vehicle.id}' #This line should be removed from here
            })
        return JsonResponse(suggestions, safe=False) # return json for Jquery autocomplete
    else:
        # Normal request - render the vehicles page
        #ADD TO WISHLIST - Check if vehicles are in the user's wishlist
        if request.user.is_authenticated:
            wishlist_vehicles = WishlistItem.objects.filter(user=request.user).values_list('vehicle_id', flat=True)
        else:
            wishlist_vehicles = []
        return render(request, 'vehicles.html', {'vehicles': vehicles, 'wishlist_vehicles': wishlist_vehicles, 'term': query})

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')

# BOOKING PAGE VIEW
def booking(request):
    vehicle_id = request.GET.get('vehicle_id')
    if not vehicle_id:
        return redirect('vehicles')

    vehicle = get_object_or_404(Vehicles, pk=vehicle_id)
    vehicle.image_url = vehicle.image.url if vehicle.image else None

    if request.method == 'POST':
        if not request.user.is_authenticated:
            # If user is not authenticated, redirect to login page or show an error
            return redirect('login') # Or render a page with an error message
        print("POST request received")  # Debugging line
        form = CreateBookingsForm(request.POST)

        if form.is_valid():
            print("Form is valid") # Debugging line

            # Manually retrieve data from the POST request
            booking_date = request.POST.get('startDate')
            pickup_location = request.POST.get('pickupLocation')
            dropoff_location = request.POST.get('dropoffLocation')
            total_price_str = request.POST.get('totalPrice') # Get as string first
            name = request.POST.get('name')
            email = request.POST.get('email')
            phone = request.POST.get('phone')
            special_requests = request.POST.get('specialRequests')
            pickup_pin_coordinates = request.POST.get('pickupPinCoordinates')
            dropoff_pin_coordinates = request.POST.get('dropoffPinCoordinates')

            print(f"Booking Date: {booking_date}") # see the vars
            print(f"Total Price (String): {total_price_str}")

            # Convert total_price to Decimal safely
            try:
                total_price = Decimal(total_price_str)
            except (TypeError, ValueError):
                print("Error: Could not convert total_price to Decimal")
                total_price = Decimal('0.00') # Or set a default value
            # Create the CustomerBookedVehicles instance
            booking = CustomerBookedVehicles(
                customer=request.user,
                vehicle=vehicle,
                booking_date=booking_date,
                pickup_location=pickup_location,
                dropoff_location=dropoff_location,
                total_price=total_price,
                name=name,
                email=email,
                phone=phone,
                specialRequests=special_requests,
                pickup_pin_coordinates=pickup_pin_coordinates,
                dropoff_pin_coordinates=dropoff_pin_coordinates,
            )

            booking.save() # save the booking
            booking_id = booking.id #get the id

            # Redirect to the confirmation page
            return redirect(reverse('booking_confirmation') + f'?booking_id={booking_id}')

        else:
            print("Form is NOT valid") # Debugging line
            print(form.errors)  # Print form errors to the console
            return render(request, 'booking.html', {'vehicle': vehicle, 'form': form})

    else:
        form = CreateBookingsForm()

    vehicle.image_url = vehicle.image.url if vehicle.image else None

    return render(request, 'booking.html', {'vehicle': vehicle, 'form': form})
# BOOKING PAGE VIEW

# BOOKING CONFIRMATION VIEW
def booking_confirmation(request):
    booking_id = request.GET.get('booking_id')
    if not booking_id:
        return redirect('home')

    booking = get_object_or_404(CustomerBookedVehicles, pk=booking_id)

    return render(request, 'booking_confirmation.html', {'booking': booking})
# BOOKING CONFIRMATION VIEW

# REGISTER VIEWS
def register_customer(request):
    if request.method == 'POST':
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = CustomerRegistrationForm()
    return render(request, 'register_customer.html', {'form': form})

def register_owner(request):
    if request.method == 'POST':
        form = OwnerRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = OwnerRegistrationForm()
    return render(request, 'register_owner.html', {'form': form})
# REGISTER VIEWS

# LOGIN LOGOUT VIEWS
def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                return render(request, 'login.html', {'form': form, 'error': 'Invalid username or password'})

    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('home')
# LOGIN LOGOUT VIEWS

# BOOKED VEHICLES PAGE VIEW
@login_required
def booked_vehicles(request):
    if request.user.is_customer:
        booked_vehicles = CustomerBookedVehicles.objects.filter(customer=request.user).order_by('-booking_date')
        return render(request, 'booked_vehicles.html', {'booked_vehicles': booked_vehicles})
    else:
        #return HttpResponse("Owners cannot access this page.")
        return render(request, 'booked_vehicles.html', {'booked_vehicles': []})
# BOOKED VEHICLES PAGE VIEW

# OWNER VEHICLE VIEWS
@login_required
def my_vehicles(request):
    if request.user.is_owner:
        vehicles = Vehicles.objects.filter(owner=request.user)
        return render(request, 'my_vehicles.html', {'vehicles': vehicles})
    else:
        return HttpResponse("Customers cannot access this page.")

@login_required
def add_vehicle(request):
    if not request.user.is_owner:
        return HttpResponse("Only owners can add vehicles.")

    if request.method == 'POST':
        form = VehicleForm(request.POST, request.FILES)
        if form.is_valid():
            vehicle = form.save(commit=False)
            vehicle.owner = request.user
            vehicle.save()
            return redirect('my_vehicles')  # Redirect to the owner's vehicle list
    else:
        form = VehicleForm()
    return render(request, 'add_vehicle.html', {'form': form, })

@login_required
def edit_vehicle(request, vehicle_id):
    vehicle = get_object_or_404(Vehicles, pk=vehicle_id, owner=request.user)

    if request.method == 'POST':
        form = VehicleForm(request.POST, request.FILES, instance=vehicle)
        if form.is_valid():
            form.save()
            return redirect('my_vehicles')
    else:
        form = VehicleForm(instance=vehicle)
    return render(request, 'edit_vehicle.html', {'form': form, 'vehicle': vehicle})

@login_required
def delete_vehicle(request, vehicle_id):
    vehicle = get_object_or_404(Vehicles, pk=vehicle_id, owner=request.user)
    vehicle.delete()
    return redirect('my_vehicles')

@login_required
def owner_bookings(request):
    if request.user.is_owner:
        # Get the vehicles that are owned by the current user
        vehicles = Vehicles.objects.filter(owner=request.user)
        # Then get the bookings that are related to the vehicles the user owns
        bookings = CustomerBookedVehicles.objects.filter(vehicle__in=vehicles).order_by('-booking_date') # order booking date descending. recent to old
        return render(request, 'owner_bookings.html', {'bookings': bookings})
    else:
         return render(request, 'owner_bookings.html', {'bookings': []})
# OWNER VEHICLE VIEWS

def one_off_data_migration(request):
    from website.models import Vehicles, User

    # Check if there's at least one user. If there are no users, create one first.
    if not User.objects.exists():
        # You can create a default user here, or prompt the admin to create one
        # For demonstration purposes, let's create a default user:
        User.objects.create_superuser('default_admin', 'default_admin@example.com', 'default_password')

    # Now get the first user to assign as the owner
    default_owner = User.objects.first()

    if default_owner:
        # Update all existing Vehicles objects to have this owner
        Vehicles.objects.filter(owner__isnull=True).update(owner=default_owner) # Only update if owner is null
        return HttpResponse("Data migration complete.")
        # return render(request, 'data_migration_complete.html')  # Or redirect
    else:
        return HttpResponse("No default user found. Create a user first.")

# ADD TO WISHLIST VIEWS
@login_required
def add_to_wishlist(request, vehicle_id):
    vehicle = get_object_or_404(Vehicles, pk=vehicle_id)
    try:
        WishlistItem.objects.create(user=request.user, vehicle=vehicle)
    except:
        pass #ADD TO WISHLIST - if already exist . dont add

    return redirect('vehicles')  # Redirect back to vehicles page

@login_required
def remove_from_wishlist(request, vehicle_id):
    vehicle = get_object_or_404(Vehicles, pk=vehicle_id)
    WishlistItem.objects.filter(user=request.user, vehicle=vehicle).delete()
    return redirect(request.META.get('HTTP_REFERER', 'vehicles'))#ADD TO WISHLIST - Redirect back to the same page

@login_required
def wishlist(request):
    wishlist_items = WishlistItem.objects.filter(user=request.user)
    return render(request, 'wishlist.html', {'wishlist_items': wishlist_items})
# ADD TO WISHLIST VIEWS