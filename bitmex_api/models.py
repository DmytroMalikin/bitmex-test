from django.db import models


class Account(models.Model):
    name = models.CharField(max_length=100, unique=True)
    api_key = models.CharField(max_length=200)
    api_secret = models.CharField(max_length=200)

    class Meta:
        verbose_name = "Account"
        verbose_name_plural = "Accounts"

    def __str__(self):
        return self.name


class Order(models.Model):
    side_validation_types = ('Buy', 'Sell')
    SIDE_TYPES = (
        (side_validation_types[0], False),
        (side_validation_types[1], True)
    )

    order_id = models.CharField(max_length=200)
    symbol = models.CharField(max_length=200)
    volume = models.CharField(max_length=200)

    side = models.BooleanField(choices=SIDE_TYPES, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    price = models.FloatField()
    account = models.ForeignKey(Account, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Order"
        verbose_name_plural = "Orders"
