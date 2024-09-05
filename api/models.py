from django.db import models

# Create your models here.
#Customer: Represents the customer who takes loans
class Customer(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)

    def __str__(self):
        return self.name

class Loan(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='loans')
    principal_amount = models.DecimalField(max_digits=12, decimal_places=2)
    rate_of_interest = models.DecimalField(max_digits=5, decimal_places=2)
    loan_period = models.IntegerField()  # in years
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)
    emi_left = models.IntegerField()
    balance_amount = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return f'Loan {self.id} for {self.customer.name}'

class Transaction(models.Model):
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE, related_name='transactions')
    date = models.DateField(auto_now_add=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    PAYMENT_TYPE_CHOICES = [
        ('EMI', 'EMI Payment'),
        ('LUMP_SUM', 'Lump Sum Payment'),
    ]
    type = models.CharField(max_length=10, choices=PAYMENT_TYPE_CHOICES)

    def __str__(self):
        return f'{self.type} of {self.amount} for Loan {self.loan.id}'
