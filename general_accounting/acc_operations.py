from .models import TrialBalance, OperativeAccounts, Assets, Passives

# popular chain of operations
# class operationsChains:


    # A+ P+
def AD_PC(acc1, acc2, value):
    Assets.objects.create(op_acc=acc1, debit_value=value)
    Passives.objects.create(op_acc=acc2, credit_value=value)

# A+ A-   
def AD_AC(acc1, acc2, value):
    Assets.objects.create(op_acc=acc, debit_value=value)
    Assets.objects.create(op_acc=acc, credit_value=value)

# P+ P-
def PD_PC(acc1, acc2, value):
    Passives.objects.create(op_acc=acc, debit_value=value)
    Passives.objects.create(op_acc=acc, credit_value=value)

# A- P-
def AC_PD(acc1, acc2, value):
    Assets.objects.create(op_acc=acc1, credit_value=value)
    Passives.objects.create(op_acc=acc2, debit_value=value)


def get_op_acc_by_number(num):
    OperativeAccounts.objects.get(number=str(num))

# in this funcs we actually describe double_account_sign ( проводка ) 
def payment_to_suppliers_for_all(value):
    """ Перечислены денежные средства поставщикам за лекарственные средства и сопутствующие товары """
    AC_PD(acc1=get_op_acc_by_number(311), acc2=get_op_acc_by_number(631), value=value) # 12

def communal_month_payment(value):
    """ Перечислены денежные средства за коммунальные услуги за текущий месяц """
    AC_PD(acc1=get_op_acc_by_number(311), acc2=get_op_acc_by_number(377), value=value) # 13

def transfer_communal_month_payment_NDS(value):
    """ Перечислены денежные средства за коммунальные услуги за текущий месяц """
    PD_PC(acc1=get_op_acc_by_number(641), acc2=get_op_acc_by_number(644), value=value) # 14 

def transfer_to_administrative_expenses(value):
    """Отнесена к административным расходам стоимость аренды и коммунальных услуг"""
    AD_PC(acc1=get_op_acc_by_number(92), acc2=get_op_acc_by_number(377), value=value) # 15

def communal_month_payment_NDS(value):
    """Отражены расчеты по налоговому кредиту по НДС""""
    PD_PC(acc1=get_op_acc_by_number(644), acc2=get_op_acc_by_number(377), value=value) # 16


# def expenses(provider_costs, communal_services_costs, c_s_NDS, administr_exp_transfer, a_e_t_NDS):
#     AC_PD(acc1=get_op_acc_by_number(311), acc1=get_op_acc_by_number(631), value=provider_costs) # 12
#     AC_PD(acc1=get_op_acc_by_number(311), acc1=get_op_acc_by_number(377), value=communal_services_costs) # 13
#     PD_PC(acc1=get_op_acc_by_number(641), acc1=get_op_acc_by_number(644), value=c_s_NDS) # 14 
#     AD_PC(acc1=get_op_acc_by_number(92), acc1=get_op_acc_by_number(377), value=administr_exp_transfer) # 15
#     PD_PC(acc1=get_op_acc_by_number(644), acc1=get_op_acc_by_number(377), value=a_e_t_NDS) # 16
    
# def profit(profit_in_cash, communal_services_costs, c_s_NDS, administr_exp_transfer, a_e_t_NDS):
#     AD_PC(acc1=get_op_acc_by_number(301), acc1=get_op_acc_by_number(702), value=profit_in_cash) # 17
#     AC_PD(acc1=get_op_acc_by_number(311), acc1=get_op_acc_by_number(377), value=communal_services_costs) # 18
#     PD_PC(acc1=get_op_acc_by_number(641), acc1=get_op_acc_by_number(644), value=c_s_NDS) # 19
#     AD_PC(acc1=get_op_acc_by_number(92), acc1=get_op_acc_by_number(377), value=administr_exp_transfer) # 20
#     PD_PC(acc1=get_op_acc_by_number(644), acc1=get_op_acc_by_number(377), value=a_e_t_NDS) # 21


# def test():
#     op_number_from = 
#     OperativeAccounts.objects.get(number=number)
#     AD_PC(100, 100)
#     AD_AC(5, 5)