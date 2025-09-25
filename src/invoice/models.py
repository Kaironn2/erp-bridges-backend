from django.db import models

from buy_order.models import Company


class Invoice(models.Model):
    access_key = models.CharField(max_length=44, unique=True)
    number = models.CharField(max_length=20)
    operation_nature = models.CharField(max_length=255)
    cfop = models.CharField(max_length=10)
    issue_date = models.DateField()
    company = models.ForeignKey(Company, models.PROTECT, related_name='invoices')
    shipping_amount = models.DecimalField(max_digits=12, decimal_places=2)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)

    recipient_cpf = models.CharField(max_length=11, null=True, blank=True)
    recipient_name = models.CharField(max_length=255)
    recipient_phone = models.CharField(max_length=20, null=True, blank=True)
    recipient_email = models.EmailField(null=True, blank=True)
    recipient_street = models.CharField(max_length=255)
    recipient_street_number = models.CharField(max_length=20)
    recipient_complement = models.CharField(max_length=255, null=True, blank=True)
    recipient_neighborhood = models.CharField(max_length=100)
    recipient_city = models.CharField(max_length=100)
    recipient_state = models.CharField(max_length=2)
    recipient_zip_code = models.CharField(max_length=8)
    recipient_country = models.CharField(max_length=100)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'NF'
        verbose_name_plural = 'NFs'

    def __str__(self):
        return f'Invoice {self.number}'
