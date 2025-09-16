from django.db import models

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
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT, related_name='buy_order')
    order_number = models.CharField(unique=True)
    order_id = models.IntegerField(unique=True)
    order_date = models.DateTimeField()
    status = models.ForeignKey(Status, models.PROTECT, related_name='buy_order')
    payment_type = models.ForeignKey(
        PaymentType,
        models.PROTECT,
        related_name='buy_order',
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
