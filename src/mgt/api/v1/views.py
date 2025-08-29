from django.db.models import Count, Sum
from rest_framework import viewsets

from mgt.models import BuyOrderDetail, Customer

from .filters import CustomerFilter
from .serializers import BuyOrderDetailSerializer, CustomerSerializer


class CustomerViewSet(viewsets.ModelViewSet):
    serializer_class = CustomerSerializer
    filterset_class = CustomerFilter

    def get_queryset(self):
        return Customer.objects.annotate(
            total_orders=Count('buy_orders'),
            total_spent=Sum('buy_orders__buy_order_detail__total_amount'),
        )


class BuyOrderViewSet(viewsets.ModelViewSet):
    queryset = BuyOrderDetail.objects.select_related().all()
    serializer_class = BuyOrderDetailSerializer
