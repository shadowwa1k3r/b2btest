import pytest
from rest_framework import status
from rest_framework.test import APIClient
from main.models import Wallet, Transaction
from decimal import Decimal
from django.urls import reverse

@pytest.fixture
def api_client():
    client = APIClient()
    client.defaults['HTTP_ACCEPT'] = 'application/vnd.api+json'
    return client

@pytest.fixture
def wallet():
    return Wallet.objects.create(label='test')

@pytest.fixture
def transaction_1(wallet):
    return Transaction.objects.create(wallet=wallet, tx_id='test1', amount=Decimal('1.00'))


@pytest.mark.django_db
def test_transaction_create(api_client, wallet):
    url = reverse('transaction-list-create')
    transaction_data = {"data": {"type": "Transaction","attributes": {"tx_id": "test", "amount": "1.00"}, "relationships": {"wallet": {"data": {"type": "Wallet", "id": wallet.id}}}}}
    response = api_client.post(url, transaction_data)
    assert response.status_code == status.HTTP_201_CREATED
    assert Transaction.objects.count() == 1
    assert Transaction.objects.get().tx_id == 'test'
    assert Transaction.objects.get().amount == Decimal('1.00')
    assert Transaction.objects.get().wallet == wallet

@pytest.mark.django_db
def test_transaction_list(api_client, wallet, transaction_1):
    url = reverse('transaction-list-create')
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data['results'][0]['tx_id'] == 'test1'
    assert response.data['results'][0]['amount'] == '1.00'
    assert response.data['results'][0]['wallet']['id'] == str(wallet.id)

@pytest.mark.django_db
def test_transaction_detail(api_client, wallet, transaction_1):
    url = reverse('transaction-detail-update-delete', kwargs={'id': transaction_1.id})
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data['tx_id'] == 'test1'
    assert response.data['amount'] == '1.00'
    assert response.data['wallet']['id'] == str(wallet.id)

@pytest.mark.django_db
def test_transaction_update(api_client, wallet, transaction_1):
    url = reverse('transaction-detail-update-delete', kwargs={'id': transaction_1.id})
    transaction_data = {"data": {"type": "Transaction", "id": transaction_1.id, "attributes": {"tx_id": "test2", "amount": "2.00"}, "relationships": {"wallet": {"data": {"type": "Wallet", "id": wallet.id}}}}}
    response = api_client.put(url, transaction_data)
    assert response.status_code == status.HTTP_200_OK
    assert Transaction.objects.count() == 1
    assert Transaction.objects.get().tx_id == 'test2'
    assert Transaction.objects.get().amount == Decimal('2.00')
    assert Transaction.objects.get().wallet == wallet

@pytest.mark.django_db
def test_transaction_delete(api_client, wallet, transaction_1):
    url = reverse('transaction-detail-update-delete', kwargs={'id': transaction_1.id})
    response = api_client.delete(url)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert Transaction.objects.count() == 0