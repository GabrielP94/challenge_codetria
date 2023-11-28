from django.db.models import Sum

from core.models import Movement


def get_account_balance(account_id):
    cash_in_movements = Movement.objects.filter(account_id=account_id,
                                                movement_type="cash_inflow"
                                                ).aggregate(Sum('amount'))

    cash_out_movements = Movement.objects.filter(account_id=account_id,
                                                 movement_type="cash_outflow"
                                                 ).aggregate(Sum('amount'))

    cash_in = 0.0 if not cash_in_movements["amount__sum"] else float(cash_in_movements["amount__sum"])
    cash_out = 0.0 if not cash_out_movements["amount__sum"] else float(cash_out_movements["amount__sum"])

    balance = cash_in - cash_out

    return balance
