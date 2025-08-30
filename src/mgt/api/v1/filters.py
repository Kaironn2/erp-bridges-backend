from django.db.models import Q, QuerySet
from django_filters import rest_framework as filters

from mgt.models import Customer


class CustomerFilter(filters.FilterSet):
    total_spent_min = filters.NumberFilter(field_name='total_spent', lookup_expr='gte')
    total_spent_max = filters.NumberFilter(field_name='total_spent', lookup_expr='lte')

    total_orders_min = filters.DateTimeFilter(field_name='total_orders', lookup_expr='gte')
    total_orders_max = filters.DateTimeFilter(field_name='total_orders', lookup_expr='lte')

    last_order_min = filters.NumberFilter(field_name='last_order', lookup_expr='gte')
    last_order_max = filters.NumberFilter(field_name='last_order', lookup_expr='lte')

    name = filters.CharFilter(method='filter_by_full_name', label='Search by name')
    email = filters.CharFilter(lookup_expr='icontains')
    cpf = filters.CharFilter(lookup_expr='icontains')
    phone = filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Customer
        fields = ['customer_group', 'state', 'country', 'postal_code']

    def filter_by_full_name(
        self, queryset: QuerySet[Customer], name: str, value: str
    ) -> QuerySet[Customer]:
        """
        Custom filter method to search by a single 'name' parameter
        across both first_name and last_name fields.
        """
        return queryset.filter(Q(first_name__icontains=value) | Q(last_name__icontains=value))
