from rest_framework import serializers

from mgt.models import Customer, CustomerGroup


class CustomerGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerGroup
        fields = ['id', 'name']


class CustomerSerializer(serializers.ModelSerializer):
    customer_group = CustomerGroupSerializer(read_only=True)
    total_orders = serializers.IntegerField(read_only=True)
    total_spent = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = Customer
        fields = [
            'id',
            'external_id',
            'first_name',
            'last_name',
            'email',
            'cpf',
            'phone',
            'customer_group',
            'customer_since',
            'postal_code',
            'city',
            'state',
            'country',
            'last_order',
            'total_orders',
            'total_spent',
        ]
