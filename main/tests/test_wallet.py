from decimal import Decimal

import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from main.models import Transaction, Wallet


@pytest.fixture
def api_client():
    client = APIClient()
    client.defaults["HTTP_ACCEPT"] = "application/vnd.api+json"
    return client


@pytest.fixture
def wallet():
    return Wallet.objects.create(label="test")


@pytest.fixture
def transaction_1(wallet):
    return Transaction.objects.create(
        wallet=wallet, tx_id="test1", amount=Decimal("1.00")
    )


@pytest.fixture
def transaction_2(wallet):
    return Transaction.objects.create(
        wallet=wallet, tx_id="test2", amount=Decimal("2.00")
    )


@pytest.fixture
def transaction_3(wallet):
    return Transaction.objects.create(
        wallet=wallet, tx_id="test3", amount=Decimal("-1.00")
    )


@pytest.mark.django_db
def test_wallet_create(api_client):
    url = reverse("wallet-list-create")
    wallet_data = {"data": {"type": "Wallet", "attributes": {"label": "test"}}}
    response = api_client.post(url, wallet_data)
    assert response.status_code == status.HTTP_201_CREATED
    assert Wallet.objects.count() == 1
    assert Wallet.objects.get().label == "test"


@pytest.mark.django_db
def test_wallet_list(api_client, wallet, transaction_1, transaction_2, transaction_3):
    url = reverse("wallet-list-create")
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data["results"][0]["id"] == wallet.id
    assert response.data["results"][0]["label"] == wallet.label
    assert response.data["results"][0]["balance"] == wallet.balance


@pytest.mark.django_db
def test_wallet_detail(api_client, wallet, transaction_1, transaction_2, transaction_3):
    url = reverse("wallet-detail-update-delete", kwargs={"id": wallet.id})
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data["id"] == wallet.id
    assert response.data["label"] == wallet.label
    assert response.data["balance"] == wallet.balance


@pytest.mark.django_db
def test_wallet_update(api_client, wallet, transaction_1, transaction_2, transaction_3):
    url = reverse("wallet-detail-update-delete", kwargs={"id": wallet.id})
    wallet_data = {
        "data": {"type": "Wallet", "id": wallet.id, "attributes": {"label": "test2"}}
    }
    response = api_client.put(url, wallet_data)
    assert response.status_code == status.HTTP_200_OK
    assert Wallet.objects.count() == 1
    assert Wallet.objects.get().label == "test2"


@pytest.mark.django_db
def test_wallet_delete(api_client, wallet, transaction_1, transaction_2, transaction_3):
    url = reverse("wallet-detail-update-delete", kwargs={"id": wallet.id})
    response = api_client.delete(url)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert Wallet.objects.count() == 0
    assert Transaction.objects.filter(wallet=wallet).count() == 0
