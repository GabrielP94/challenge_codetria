from django.db.models import Sum

from core.models import Movement


def get_account_balance(account_id):
    cash_in = Movement.objects.filter(account_id=account_id,
                                      movement_type="cash_inflow").aggregate(Sum('amount'))["amount__sum"]

    cash_out = Movement.objects.filter(account_id=account_id,
                                       movement_type="cash_outflow").aggregate(Sum('amount'))["amount__sum"]
    balance = 0.0 if not cash_in else float(cash_in) - 0.0 if not cash_out else float(cash_out)

    return balance