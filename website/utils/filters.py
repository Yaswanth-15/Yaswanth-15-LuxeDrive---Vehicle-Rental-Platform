# utils/filters.py

from django.db.models import Q
from website.models import Vehicles

class VehicleFilter:
    def __init__(self, query_params):
        self.query_params = query_params
        self.queryset = Vehicles.objects.all()  # Start with all vehicles

    def filter_by_search(self):
        search_query = self.query_params.get('search', '')
        if search_query:
            self.queryset = self.queryset.filter(
                Q(name__icontains=search_query) |  # Search in name
                Q(description__icontains=search_query) # Search in description
            )

    def filter_by_price_range(self):
        price_range = self.query_params.get('price_range', '')
        if price_range == 'cheap':
            self.queryset = self.queryset.filter(price__lt=1000)
        elif price_range == 'mid':
            self.queryset = self.queryset.filter(price__gte=10000, price__lte=5000)
        elif price_range == 'expensive':
            self.queryset = self.queryset.filter(price__gt=5000)

    def apply_filters(self):
        # Apply all filters
        self.filter_by_search()
        self.filter_by_price_range()
        return self.queryset