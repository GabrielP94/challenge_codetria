import factory

from core.models import Account
from core.models import Category
from core.models import Client
from core.models import Movement


class ClientFactory(factory.Factory):
    class Meta:
        model = Client

    name = "Cosme Fulanito"


class CategoryFactory(factory.Factory):
    class Meta:
        model = Category

    name = "Categoria 1"


class AccountFactory(factory.Factory):
    class Meta:
        model = Account


class MovementFactory(factory.Factory):
    class Meta:
        model = Movement

    account = 1
    movement_type = "cash_inflow"
    amount = 1000.0
