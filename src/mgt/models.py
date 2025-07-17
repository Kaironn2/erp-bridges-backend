from django.db import models


class CustomerGroup(models.Model):
    name = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Grupo de Clientes'
        verbose_name_plural = 'Grupos de Clientes'

    def __str__(self):
        return self.name


class Customer(models.Model):
    external_id = models.CharField(unique=True, blank=True, null=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True)
    cpf = models.CharField(max_length=20, unique=True, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    customer_group = models.ForeignKey(
        CustomerGroup, on_delete=models.PROTECT, related_name='customers'
    )
    customer_since = models.DateTimeField(blank=True, null=True)
    postal_code = models.CharField(max_length=20, blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    state = models.CharField(max_length=255, blank=True, null=True)
    last_order = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'

        indexes = [
            models.Index(fields=['cpf', 'email']),
        ]

    def __str__(self):
        return self.email


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
    order_number = models.CharField(unique=True)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT, related_name='buy_orders')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Ordem de Compra'
        verbose_name_plural = 'Ordens de Compra'

    def __str__(self):
        return str(self.order_number)


class BuyOrderDetail(models.Model):
    buy_order = models.OneToOneField(
        BuyOrder, on_delete=models.CASCADE, related_name='buy_order_detail'
    )
    order_external_id = models.IntegerField(unique=True)
    order_date = models.DateTimeField()
    status = models.ForeignKey(Status, models.PROTECT, related_name='buy_orders_details')
    payment_type = models.ForeignKey(
        PaymentType,
        models.PROTECT,
        related_name='buy_orders_details',
    )
    shipping_amount = models.DecimalField(max_digits=10, decimal_places=2)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Detalhe da Ordem de Compra'
        verbose_name_plural = 'Detalhes das Ordens de Compra'

    def __str__(self):
        return f'Buy Order {self.buy_order.order_number} detail'
