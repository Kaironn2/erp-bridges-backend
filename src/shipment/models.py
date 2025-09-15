from django.db import models

from mgt.models import BuyOrder


class ShippingType(models.Model):
    class ShippingTypeChoices(models.TextChoices):
        ENTREGA = 'entrega', 'Entrega'
        RETIRADA = 'retirada', 'Retirada'

    name = models.CharField(unique=True)
    type = models.CharField(
        max_length=10,
        choices=ShippingTypeChoices.choices,
    )
    extra_deadline_days = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Tipo de Entrega'
        verbose_name_plural = 'Tipos de Entrega'


class Shipment(models.Model):
    buy_order = models.OneToOneField(BuyOrder, on_delete=models.CASCADE, related_name='shipment')
    deadline_days = models.PositiveIntegerField()
    customer_deadline = models.DateField(blank=True, null=True)
    shipping_deadline = models.DateField(blank=True, null=True)
    tracking_code = models.CharField(max_length=100, null=True, blank=True)
    pickup_date = models.DateField(null=True, blank=True)
    delivered_at = models.DateField(null=True, blank=True)
    shipping_type = models.ForeignKey(
        ShippingType, on_delete=models.PROTECT, related_name='shipment'
    )
    shipping_city = models.CharField(max_length=100)
    shipping_state = models.CharField(max_length=50)
    shipping_zip_code = models.CharField(max_length=50)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Pedido {self.buy_order.order_number} - {self.tracking_code or "no tracking code"}'

    class Meta:
        verbose_name = 'Entrega'
        verbose_name_plural = 'Entregas'
