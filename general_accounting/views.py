from django.shortcuts import render
# from .acc_operations import (payment_to_suppliers_for_all, communal_month_payment, transfer_communal_month_payment_NDS, transfer_to_administrative_expenses, communal_month_payment_NDS)
# Create your views here.
from .models import Assets, Passives, OperativeAccounts, TrialBalance, AccountingBalance
from django.urls import reverse_lazy
from simulation.models import get_simulation

def accounting_main_page(request):
    if get_simulation() is not False:
        simulations_exists = True
    context = {
        "simulations_exists": simulations_exists
    }
    return render(request, 'accounting_main_page.html', context)

# def perform_operations(request):
#     """ робота бухгалтера (его имитация) """
#     # по началу со статичными значениями для проверки

#     #populate ASsets and Passives 
#     # payment_to_suppliers_for_all(value=268500)
#     # communal_month_payment(value=4800)
#     # transfer_communal_month_payment_NDS(value=800)
#     # transfer_to_administrative_expenses(value=4000)
#     # communal_month_payment_NDS(value=800)
#     #ASsets and Passives are populated now
#     # NOOOOO!
#     # and then immidiatly show trial_balance
#     # return render(request, reverse_lazy('trial_balance', args=None, kwargs=None))
#     # NOOOOO!
#     # go back
#     return render(request, reverse_lazy('accounting_main_page'))

def list_of_tbs(request):
    context = {}
    if TrialBalance.objects.order_by("id").filter(reported=True).exists():
        tbs = TrialBalance.objects.order_by("id").filter(reported=True)
        ids = [tb.id for tb in tbs]
        dates_reported = [tb.date_report for tb in tbs]
        data = zip(ids, dates_reported)
        context = {
            "data": data,
            "exists": True
        }
    else:
        context = {
            "exists": False
        }
    return render(request, 'list_of_tbs.html', context=context)

def list_of_abs(request):
    context = {}
    if AccountingBalance.objects.order_by("id").filter(reported=True).exists():
        accbs = AccountingBalance.objects.order_by("id").filter(reported=True)
        ids = [ab.id for ab in accbs]
        dates_reported = [ab.date_report for ab in accbs]
        data = zip(ids, dates_reported)
        context = {
            "data": data,
            "exists": True
        }
    else:
        context = {
            "exists": False
        }
    return render(request, 'list_of_abs.html', context=context)

def certain_tb(request, id):
    context = {}
    try:
        tb = TrialBalance.objects.get(id=id)
        if tb.reported == True:
            list_dict_data = tb.get_dicts_of_accs()
            list_dict_data_keys = [key for key in (list_dict_data[0]).keys()]
            context = {
                "list_dict_data": list_dict_data,
                "list_dict_data_keys": list_dict_data_keys,
                "start_saldo_credit": tb.start_saldo_credit,
                "start_saldo_debit": tb.start_saldo_debit,
                "end_saldo_debit": tb.end_saldo_debit,
                "end_saldo_credit": tb.end_saldo_credit,
                "turnover_credit": tb.turnover_credit,
                "turnover_debit": tb.turnover_debit,
                "performed": True
            }
        else:
            context = {
                "performed": False
            }
    except Exception:
        print(f'\n\nThere is no TrialBalance {id} in system (try to create it before call)\n')
        context = {
            "performed": False
        }
    return render(request, 'trial_balance.html', context=context)

def certain_ab(request, id):
    context = {}
    try:
        ab = AccountingBalance.objects.get(id=id)
        assets = ab.get_assets()
        passives = ab.get_passives()
        if ab.reported == True:
            context = {
                "period": ab.period, # in days
                "date_reported": ab.date_report,
                "assets": assets,
                "passives": passives, # in html if statement to show is balance ok on not
                "assets_total": ab.assets_total,
                "passives_total": ab.passives_total,
                "performed": True
            }
        else:
            context = {
                "performed": False
            }
    except Exception:
        print(f'\n\nThere is no AccountingBalance {id} in system (try to create it before call)\n')
        context = {
            "performed": False
        }
    return render(request, 'accounting_balance.html', context)

def get_accounting_balance(request):
    """ Бухгалтерский баланс """

    ab = AccountingBalance.objects.order_by("id").last()
    assets = ab.get_assets()
    passives = ab.get_passives()
    answer = ab.get_report() # to create next AB instance and poopulate some fields (period, ...)
    ab.refresh_from_db()
    context = {}
    if answer:
        context = {
            "period": ab.period, # in days
            "date_reported": ab.date_report,
            "assets": assets,
            "passives": passives, # in html if statement to show is balance ok on not
            "assets_total": ab.assets_total,
            "passives_total": ab.passives_total,
            "performed": answer
        }
    else:
        context = {
            "performed": answer
        }
    return render(request, 'accounting_balance.html', context)


def get_trial_balance(request):
    """Оборотно-сальдовая ведомость"""
    tb = TrialBalance.objects.order_by("id").last()
    answer = tb.get_report()
    context = {}
    if answer:
        tb.refresh_from_db()
        list_dict_data = tb.get_dicts_of_accs()
        list_dict_data_keys = [key for key in (list_dict_data[0]).keys()]
        context = {
            "list_dict_data": list_dict_data,
            "list_dict_data_keys": list_dict_data_keys,
            "start_saldo_credit": tb.start_saldo_credit,
            "start_saldo_debit": tb.start_saldo_debit,
            "end_saldo_debit": tb.end_saldo_debit,
            "end_saldo_credit": tb.end_saldo_credit,
            "turnover_credit": tb.turnover_credit,
            "turnover_debit": tb.turnover_debit,
            "performed": answer
            # "turnover": turnover, # обороты за период # all (credit + debit) money for that time
            # "period": period, # in days
            # "saldo_start": saldo_start,
            # "saldo_end": saldo_end,
            # "actives_value": actives_value,
            # "passives_value": passives_value, # in html if statement to show is balance ok on not
        }
    else:
        context = {
            "performed": answer
        }
    return render(request, 'trial_balance.html', context=context)