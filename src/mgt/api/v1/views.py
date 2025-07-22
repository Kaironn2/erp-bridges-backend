from django.db.models import Count, Sum
from rest_framework import viewsets

from mgt.models import Customer

from .serializers import CustomerGroupSerializer


class CustomerViewSet(viewsets.ModelViewSet):
    serializer_class = CustomerGroupSerializer

    def get_queryset(self):
        return Customer.objects.annotate(
            total_orders=Count('buy_orders'),
            total_spent=Sum('buy_orders__buy_order_detail__total_amount')
        )
