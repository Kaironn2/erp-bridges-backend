from django.db import models

from mgt.models import BuyOrder


class ShippingMethod(models.Model):
    name = models.CharField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Método de Entrega'
        verbose_name_plural = 'Métodos de Entrega'


class Shipment(models.Model):
    buy_order = models.OneToOneField(BuyOrder, on_delete=models.CASCADE, related_name='shipment')

    mgt_deadline = models.DateField()
    deadline = models.DateField()
    tracking_code = models.CharField(max_length=100, null=True, blank=True)
    expedition_date = models.DateField(null=True, blank=True)
    expedition_method = models.CharField(max_length=100, null=True, blank=True)
    pickup_date = models.DateField(null=True, blank=True)
    delivered_at = models.DateField(null=True, blank=True)
    shipping_method = models.ForeignKey(
        ShippingMethod, on_delete=models.PROTECT, related_name='shipment'
    )
    shipping_city = models.CharField(max_length=100)
    shipping_state = models.CharField(max_length=50)
    shipping_zip_code = models.CharField(max_length=50)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.shipping_method} - {self.tracking_code or "no tracking code"}'

    class Meta:
        verbose_name = 'Entrega'
        verbose_name_plural = 'Entregas'
