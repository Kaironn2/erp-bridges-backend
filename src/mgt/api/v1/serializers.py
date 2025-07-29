from rest_framework import serializers

from mgt.models import BuyOrder, BuyOrderDetail, Customer, CustomerGroup, PaymentType, Status


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


class PaymentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentType
        fields = ['id', 'name']


class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = ['id', 'name']


class BuyOrderSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer(read_only=True)

    class Meta:
        model = BuyOrder
        fields = ['id', 'order_number', 'customer']


class BuyOrderDetailSerializer(serializers.ModelSerializer):
    buy_order = BuyOrderSerializer(read_only=True)
    payment_type = PaymentTypeSerializer(read_only=True)
    status = StatusSerializer(read_only=True)

    class Meta:
        model = BuyOrderDetail
        fields = [
            'id',
            'buy_order',
            'order_external_id',
            'order_date',
            'status',
            'payment_type',
            'shipping_amount',
            'discount_amount',
            'total_amount',
            'sold_quantity',
            'tracking_code',
            'created_at',
            'updated_at',
        ]
