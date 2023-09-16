from rest_framework.serializers import ModelSerializer
from rest_framework_json_api.relations import ResourceRelatedField

from .models import Transaction, Wallet


class WalletSerializer(ModelSerializer):
    class Meta:
        model = Wallet
        fields = ["id", "label", "balance"]


class TransactionSerializer(ModelSerializer):
    wallet = ResourceRelatedField(
        queryset=Wallet.objects.all(),
    )

    class Meta:
        model = Transaction
        fields = ["id", "wallet", "tx_id", "amount"]
