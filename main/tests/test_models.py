import pytest
from main.models import Wallet, Transaction
from decimal import Decimal

@pytest.fixture
def wallet():
    return Wallet.objects.create(label='test')

@pytest.fixture
def wallet_2():
    return Wallet.objects.create(label='')

@pytest.fixture
def transaction_1(wallet):
    return Transaction.objects.create(wallet=wallet, tx_id='test1', amount=Decimal('1.00'))

@pytest.fixture
def transaction_2(wallet):
    return Transaction.objects.create(wallet=wallet, tx_id='test2', amount=Decimal('2.00'))

@pytest.fixture
def transaction_3(wallet_2):
    return Transaction.objects.create(wallet=wallet_2, tx_id='test3', amount=Decimal('-1.00'))

@pytest.mark.django_db
def test_wallet_balance(wallet, transaction_1, transaction_2):
    assert wallet.balance == Decimal('3.00')

@pytest.mark.django_db
def test_transaction_str(wallet, transaction_1):
    assert str(transaction_1) == 'test 1.00'

@pytest.mark.django_db
def test_wallet_str(wallet):
    assert str(wallet) == 'test'

@pytest.mark.django_db
def test_transaction_str_without_wallet_label(wallet_2, transaction_3):
    assert str(transaction_3) == ' -1.00'