from django.db import models


class Company(models.Model):
    name = models.CharField(max_length=255)
    cnpj = models.CharField(max_length=18, unique=True)
    email = models.EmailField(blank=True, null=True)
    ie = models.CharField(blank=True, null=True, unique=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=50, blank=True, null=True)
    country = models.CharField(max_length=50, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Companhia'
        verbose_name_plural = 'Companhias'

    def __str__(self):
        return self.name


class BankAccount(models.Model):
    class AccountType(models.TextChoices):
        CHECKING = 'checking', 'Checking Account'
        SAVINGS = 'savings', 'Savings Account'
        PAYMENT = 'payment', 'Payment Account'

    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='bank_accounts')
    bank_name = models.CharField(max_length=100)
    bank_code = models.CharField(max_length=10)
    branch_number = models.CharField(max_length=10)
    branch_digit = models.CharField(max_length=1, blank=True, null=True)
    account_number = models.CharField(max_length=20)
    account_digit = models.CharField(max_length=1, blank=True, null=True)
    operation = models.CharField(
        max_length=5,
        blank=True,
        null=True,
    )
    account_type = models.CharField(
        max_length=20, choices=AccountType.choices, default=AccountType.CHECKING
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Conta Bancária'
        verbose_name_plural = 'Contas Bancárias'

    def __str__(self):
        return (
            f'{self.bank_name} - {self.branch_number}/{self.account_number}-{self.account_digit}'
        )
