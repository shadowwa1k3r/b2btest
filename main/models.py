from django.db import models

class Wallet(models.Model):
    label = models.CharField(max_length=200)

    @property
    def balance(self):
        return sum(tx.amount for tx in self.transaction_set.all())

    def __str__(self):
        return self.label

class Transaction(models.Model):
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE)
    tx_id = models.CharField(max_length=200, unique=True)
    amount = models.DecimalField(max_digits=18, decimal_places=2)

    def __str__(self):
        return f'{self.wallet.label} {self.amount}'