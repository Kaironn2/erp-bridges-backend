from django.db import models

from buy_order.models import BuyOrder


class ShipmentType(models.Model):
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Tipo de Entrega'
        verbose_name_plural = 'Tipo de Entregas'

    def __str__(self):
        return self.name


class Shipment(models.Model):
    buy_order = models.ForeignKey(
        BuyOrder,
        on_delete=models.CASCADE,
        related_name='shipments',
    )
    shipment_type = models.ForeignKey(
        ShipmentType, on_delete=models.PROTECT, related_name='shipments'
    )
    tracking_code = models.CharField(max_length=255, blank=True, null=True)
    pickup_date = models.DateField(blank=True, null=True)
    deadline = models.DateField(blank=True, null=True)
    weight = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    shipping_cost = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    delivered_at = models.DateField(blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    zip_code = models.CharField(max_length=20, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Shipment'
        verbose_name_plural = 'Shipments'

    def __str__(self):
        return f'{self.buy_order.order_number} - {self.shipment_type.name}'
