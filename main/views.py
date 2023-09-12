from django.db import transaction
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets
from .models import Transaction, Wallet

from .serializers import TransactionSerializer, WalletSerializer


class WalletViewSet(viewsets.ModelViewSet):
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer
    filterset_fields = ['label']
    search_fields = ['label']
    ordering_fields = ['id', 'label', 'balance']
    ordering = ['id']
    lookup_field = 'id'

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        # sid = transaction.savepoint()
        # transaction.savepoint_rollback(sid)
        # transaction.savepoint_commit(sid)
        # if there would be some complex logic, we could use savepoints
        # to rollback the transaction to a specific point
        # but atm, I think atomic decorator is enough
        return super().create(request, *args, **kwargs)

    @transaction.atomic
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @transaction.atomic
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, *kwargs)


class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    filterset_fields = ['wallet', 'tx_id', 'amount']
    search_fields = ['wallet__label', 'tx_id', 'amount']
    ordering_fields = ['id', 'wallet__label', 'tx_id', 'amount']
    ordering = ['id']
    lookup_field = 'id'

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @transaction.atomic
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @transaction.atomic
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, *kwargs)
