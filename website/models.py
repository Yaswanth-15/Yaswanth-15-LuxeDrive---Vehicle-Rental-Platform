from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):  # Use AbstractUser to customize
    is_customer = models.BooleanField(default=True)
    is_owner = models.BooleanField(default=False)

class Vehicles(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='vehicles', null= True)
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='Vehicles/images/')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()

    def __str__(self):
        return self.name

class CustomerBookedVehicles(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    vehicle = models.ForeignKey(Vehicles, on_delete=models.CASCADE)
    booking_date = models.DateField()
    pickup_location = models.CharField(max_length=255)
    dropoff_location = models.CharField(max_length=255)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    phone = models.CharField(max_length=20)
    specialRequests = models.TextField(blank=True, null=True)
    pickup_pin_coordinates = models.CharField(max_length=255, blank=True, null=True)
    dropoff_pin_coordinates = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.customer.username} booked {self.vehicle.name}"

#ADD TO WISHLIST - Model
class WishlistItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    vehicle = models.ForeignKey(Vehicles, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'vehicle')  # Prevent duplicate wishlist items

    def __str__(self):
        return f"{self.user.username} - {self.vehicle.name}"

#ADD TO WISHLIST - Model