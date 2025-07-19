from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from .models import User, Vehicles, CustomerBookedVehicles
import urllib
from django.core.files.base import ContentFile
from django.utils.text import slugify
from datetime import date


class CustomerRegistrationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('email', 'first_name', 'last_name')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_customer = True
        user.is_owner = False
        if commit:
            user.save()
        return user


class OwnerRegistrationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('email', 'first_name', 'last_name')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_customer = False
        user.is_owner = True
        if commit:
            user.save()
        return user


class VehicleForm(forms.ModelForm):
    image_url = forms.URLField(required=False, label="Image URL (Optional)")
    image = forms.ImageField(required=False, label="Upload Image (Optional)")

    class Meta:
        model = Vehicles
        fields = ['name', 'image', 'image_url', 'price', 'description']

    def clean(self):
        cleaned_data = super().clean()
        image = cleaned_data.get('image')
        image_url = cleaned_data.get('image_url')

        if image and image_url:
            raise ValidationError("Please provide either an image file or a URL, not both.")

        if not image and not image_url:
            raise ValidationError("Please provide either an image file or a URL.")

        return cleaned_data

    def save(self, commit=True):
        vehicle = super().save(commit=False)
        image_url = self.cleaned_data.get('image_url')
        image = self.cleaned_data.get('image')
        if image_url:
            try:
                 image_name = slugify(image_url.split('/')[-1]) or 'vehicle_image' # Slugify image name
                 image_content = urllib.request.urlopen(image_url).read()
                 vehicle.image.save(image_name, ContentFile(image_content), save=False)
            except Exception as e:
                raise ValidationError(f"Error downloading image from URL: {e}")
        else:
             vehicle.image = image

        if commit:
            vehicle.save()
        return vehicle

class CreateBookingsForm(forms.ModelForm):
    class Meta:
        model = CustomerBookedVehicles
        fields = [] # empty list

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # All fields are populated in views.py