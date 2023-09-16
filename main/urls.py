from django.urls import path

from .views import TransactionViewSet, WalletViewSet

urlpatterns = [
    path(
        "wallets/",
        WalletViewSet.as_view({"get": "list", "post": "create"}),
        name="wallet-list-create",
    ),
    path(
        "wallets/<int:id>/",
        WalletViewSet.as_view(
            {"get": "retrieve", "put": "update", "delete": "destroy"}
        ),
        name="wallet-detail-update-delete",
    ),
    path(
        "transactions/",
        TransactionViewSet.as_view({"get": "list", "post": "create"}),
        name="transaction-list-create",
    ),
    path(
        "transactions/<int:id>/",
        TransactionViewSet.as_view(
            {"get": "retrieve", "put": "update", "delete": "destroy"}
        ),
        name="transaction-detail-update-delete",
    ),
]
