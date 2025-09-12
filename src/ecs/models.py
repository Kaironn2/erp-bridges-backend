from django.db import models

from mgt.models import BuyOrder


class Company(models.Model):
    name = models.CharField(max_length=100, unique=True)
    cnpj = models.CharField(max_length=100, unique=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class EcsOrder(models.Model):
    ecs_order_number = models.CharField(max_length=50, unique=True)
    ecs_order_id = models.CharField(max_length=50, unique=True)
    buy_order = models.OneToOneField(BuyOrder, on_delete=models.CASCADE, related_name='ecs')
    payment_date = models.DateField(blank=True, null=True)
    recipient_name = models.CharField(max_length=100)
    recipient_city = models.CharField(max_length=100)
    recipient_state = models.CharField(max_length=50)
    recipient_zip_code = models.CharField(max_length=50)
    ecs_delivery_date = models.DateTimeField(blank=True, null=True)
    company = models.ForeignKey(Company, on_delete=models.PROTECT, related_name='ecs')
    coupon = models.CharField(max_length=100)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.ecs_order_number

    class Meta:
        verbose_name = 'Pedido ECS'
        verbose_name_plural = 'Pedidos ECS'
