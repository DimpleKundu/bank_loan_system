from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Customer, Loan, Transaction
from .serializers import CustomerSerializer, LoanSerializer, TransactionSerializer
from django.shortcuts import get_object_or_404
from django.db.models import Sum

# LEND: API to create a new loan
class LoanViewSet(viewsets.ViewSet):
    def create(self, request):
        customer = get_object_or_404(Customer, id=request.data['customer_id'])
        principal_amount = request.data['principal_amount']
        rate_of_interest = request.data['rate_of_interest']
        loan_period = request.data['loan_period']

        interest = (principal_amount * rate_of_interest * loan_period) / 100
        total_amount = principal_amount + interest
        emi_left = loan_period * 12  # Assuming EMI is paid monthly
        balance_amount = total_amount

        loan = Loan.objects.create(
            customer=customer,
            principal_amount=principal_amount,
            rate_of_interest=rate_of_interest,
            loan_period=loan_period,
            total_amount=total_amount,
            emi_left=emi_left,
            balance_amount=balance_amount
        )

        serializer = LoanSerializer(loan)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

# PAYMENT: API to make a payment (EMI or LUMP SUM)
class PaymentViewSet(viewsets.ViewSet):
    def create(self, request):
        loan = get_object_or_404(Loan, id=request.data['loan_id'])
        amount = request.data['amount']
        payment_type = request.data['type']

        # Create a transaction
        transaction = Transaction.objects.create(
            loan=loan,
            amount=amount,
            type=payment_type
        )

        # Update loan balance and EMI left
        loan.balance_amount -= amount
        if payment_type == 'EMI':
            loan.emi_left -= 1

        if loan.balance_amount <= 0:
            loan.balance_amount = 0
            loan.emi_left = 0

        loan.save()
        serializer = TransactionSerializer(transaction)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

# LEDGER: API to get all transactions for a loan
class LedgerViewSet(viewsets.ViewSet):
    def list(self, request, loan_id=None):
        loan = get_object_or_404(Loan, id=loan_id)
        transactions = loan.transactions.all()
        loan_serializer = LoanSerializer(loan)
        transaction_serializer = TransactionSerializer(transactions, many=True)
        return Response({
            'loan_details': loan_serializer.data,
            'transactions': transaction_serializer.data
        })

# ACCOUNT OVERVIEW: API to list all loans of a customer
class AccountOverviewViewSet(viewsets.ViewSet):
    def list(self, request, customer_id=None):
        customer = get_object_or_404(Customer, id=customer_id)
        loans = customer.loans.all()
        loan_serializer = LoanSerializer(loans, many=True)
        return Response(loan_serializer.data)

from .models import Customer
from .serializers import CustomerSerializer

class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
