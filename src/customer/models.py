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
    country = models.CharField(max_length=255, blank=True, null=True)
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
