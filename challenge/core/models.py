from django.db import models

from core.external_apis.currency_api import get_currencies_values


class BaseModel(models.Model):
    date_joined = models.DateTimeField('Create Date', auto_now=False, auto_now_add=True)
    last_update = models.DateTimeField('Modification Date', auto_now=True, auto_now_add=False)
    delete_date = models.DateTimeField('Delete Date', null=True, default=None, blank=True)
    state = models.BooleanField('State', default=True)

    class Meta:
        abstract = True
        verbose_name = 'Base Model'


class Client(models.Model):
    name = models.TextField(blank=False, null=False, default="N/D")


class Category(models.Model):
    name = models.TextField(blank=False, null=False, default="N/D")


class Account(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    balance = models.FloatField(blank=False, null=False, default=0.0)

    def get_total_usd(self):
        dollar_value = get_currencies_values("Dolar Bolsa")["casa"]["compra"].replace(",", ".")

        if dollar_value:
            return "{:.2f}".format(self.balance / float(dollar_value))
        else:
            return 0


class Movement(models.Model):
    MOVEMENT_TYPE = [
        ('cash_outflow', 'Egreso'),
        ('cash_inflow', 'Ingreso')
    ]
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    movement_type = models.CharField(max_length=20, choices=MOVEMENT_TYPE, blank=False,
                                     null=False, default='cash_inflow')
    amount = models.FloatField(null=False, blank=False, default=0.0)


class CategoryClient(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
