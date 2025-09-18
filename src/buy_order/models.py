from django.db import models

from company.models import Company
from customer.models import Customer


class PaymentType(models.Model):
    name = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Tipo de Pagamento'
        verbose_name_plural = 'Tipos de Pagamento'

    def __str__(self):
        return self.name


class Status(models.Model):
    name = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Status'
        verbose_name_plural = 'Status'

    def __str__(self):
        return self.name


class BuyOrder(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT, related_name='buy_orders')
    order_number = models.CharField(unique=True)
    order_id = models.IntegerField(unique=True)
    order_date = models.DateTimeField()
    status = models.ForeignKey(Status, models.PROTECT, related_name='buy_orders')
    payment_type = models.ForeignKey(
        PaymentType,
        models.PROTECT,
        related_name='buy_orders',
    )
    shipping_amount = models.DecimalField(max_digits=10, decimal_places=2)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    sold_quantity = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Ordem de Compra'
        verbose_name_plural = 'Ordens de Compra'

    def __str__(self):
        return f'Buy Order {self.order_number}'


class EcsBuyOrder(models.Model):
    buy_order = models.ForeignKey(
        BuyOrder, on_delete=models.CASCADE, related_name='ecs_buy_orders'
    )
    ecs_order_id = models.CharField(max_length=50)
    ecs_order_number = models.CharField(max_length=50)
    payment_date = models.DateField(blank=True, null=True)
    coupon = models.CharField(max_length=100, blank=True, null=True)
    company = models.ForeignKey(Company, on_delete=models.PROTECT, related_name='ecs_buy_orders')
    recipient_name = models.CharField(max_length=100)
    recipient_zip_code = models.CharField(max_length=8)
    recipient_city = models.CharField(max_length=100)
    recipient_state = models.CharField(max_length=2)
    ecs_delivery_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        verbose_name = 'Ecs - Ordem de Compra'
        verbose_name_plural = 'Ecs - Ordens de Compra'

    def __str__(self):
        return f'Buy Order {self.ecs_order_number}'
