import django_filters
import django_widgets as django_widgets

from django_filters import DateFilter, CharFilter

from .models import *
from django.utils.translation import gettext_lazy as _


class OrderFilter(django_filters.FilterSet):
    start_date = DateFilter(field_name="created_at", lookup_expr='gte')
    end_date = DateFilter(field_name="created_at", lookup_expr='lte')
    shipping_address = CharFilter(field_name='shipping_address', lookup_expr='icontains')

    class Meta:
        model = Order
        fields = '__all__'

        exclude = ['customer', 'date_created', 'subtotal', 'discount', 'cart', 'total']
