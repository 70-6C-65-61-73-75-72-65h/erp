from .models import TrialBalance, OperativeAccounts, Assets, Passives

# popular chain of operations
# class operationsChains:


    # A+ P+
def AD_PC(acc1, acc2, value):
    Assets.objects.create(op_acc=acc1, debit_value=value)
    Passives.objects.create(op_acc=acc2, credit_value=value)

# A+ A-   
def AD_AC(acc1, acc2, value):
    Assets.objects.create(op_acc=acc1, debit_value=value)
    Assets.objects.create(op_acc=acc2, credit_value=value)

# P+ P-
def PD_PC(acc1, acc2, value):
    Passives.objects.create(op_acc=acc1, debit_value=value)
    Passives.objects.create(op_acc=acc2, credit_value=value)

# A- P-
def AC_PD(acc1, acc2, value):
    Assets.objects.create(op_acc=acc1, credit_value=value)
    Passives.objects.create(op_acc=acc2, debit_value=value)


def get_op_acc_by_number(num):
    OperativeAccounts.objects.get(number=str(num))

# in this funcs we actually describe double_account_sign ( проводка ) 



# 1
# Purchase from vendor
# запишем с наценкой
def received_products(value):
    """Оприходованы лекарственные средства от поставщиков"""
    AD_PC(acc1=get_op_acc_by_number(282), acc2=get_op_acc_by_number(631), value=value)

# def settled_products_markup_value(value):
#     """Отражена торговая наценка (разность между продажной и покупательной стоимостью лекарственных средств)"""
#     AD_AC(acc1=get_op_acc_by_number(282), acc2=get_op_acc_by_number(285), value=value)

# заплатим по себестоимости
def payment_to_suppliers_for_all(value):
    """ Перечислены денежные средства поставщикам за лекарственные средства и сопутствующие товары """
    AC_PD(acc1=get_op_acc_by_number(311), acc2=get_op_acc_by_number(631), value=value) # 12

# 2
# WHTransfer
def fuel_spends_payment(value):
    """Оплата бензина за трансфер продуктов из '311 Текущие счета в национальной валюте' в '801 Затраты сырья и материалов'"""
    AC_PD(acc1=get_op_acc_by_number(311), acc2=get_op_acc_by_number(803), value=value)
    # из актив кредит 311 в пассив дебет 806 Затраты запасных частей - ремонт
    # из актив кредит 311 в пассив дебет 803 Затраты топлива и энергии - закупка == затраты бензина при трансфере

def vehicle_repair_spends_payment(value):
    AC_PD(acc1=get_op_acc_by_number(311), acc2=get_op_acc_by_number(806), value=value)

# 3
# Sale
def sale_to_cassa(value):
    """ Покупка пользователя наличкой """
    AD_AC(acc1=get_op_acc_by_number(311), acc2=get_op_acc_by_number(282), value=value) # 285 наценку счета не проводим ибо геморно

def sale_to_account(value):
    """ Покупка пользователя по карте """
    AD_PC(acc1=get_op_acc_by_number(311), acc2=get_op_acc_by_number(282), value=value)

# 0
#если на аккаунте предприятия закончились бабки - пеервод из касс на аккаунты
def money_cassa_to_account_transfer(value):
    AD_AC(acc1=get_op_acc_by_number(311), acc2=get_op_acc_by_number(301), value=value)
# и наоборот
def money_account_to_cassa_transfer(value):
    AD_AC(acc1=get_op_acc_by_number(301), acc2=get_op_acc_by_number(311), value=value)
# 4
# Salary
# - (селери за месяц) ДП 661 КА 311  ( сразу с налогом ), 
def salary_payment(value):
    AC_PD(acc1=get_op_acc_by_number(311), acc2=get_op_acc_by_number(661), value=value)

# 5
# Communal services
# - (коммуналка налог) ДП 377 КА 311 ( сразу с налогом ),
def communal_month_payment(value):
    """ Перечислены денежные средства за коммунальные услуги за текущий месяц """
    AC_PD(acc1=get_op_acc_by_number(311), acc2=get_op_acc_by_number(377), value=value) # 13 acc1 -> acc2

# вся цепь
# def communal_tasks(value, tax_value):
    # communal_month_payment(value)
    # transfer_communal_month_payment_NDS(tax_value)
    # transfer_to_administrative_expenses(value)
    # communal_month_payment_NDS(tax_value)

# def communal_month_payment(value):
#     """ Перечислены денежные средства за коммунальные услуги за текущий месяц """
#     AC_PD(acc1=get_op_acc_by_number(311), acc2=get_op_acc_by_number(377), value=value) # 13 acc1 -> acc2

# def transfer_communal_month_payment_NDS(value):
#     """ Перечислены денежные средства за коммунальные услуги за текущий месяц """
#     PD_PC(acc1=get_op_acc_by_number(641), acc2=get_op_acc_by_number(644), value=value) # 14  <-

# def transfer_to_administrative_expenses(value):
#     """Отнесена к административным расходам стоимость аренды и коммунальных услуг"""
#     AD_PC(acc1=get_op_acc_by_number(92), acc2=get_op_acc_by_number(377), value=value) # 15 <-

# def communal_month_payment_NDS(value):
#     """Отражены расчеты по налоговому кредиту по НДС""""
#     PD_PC(acc1=get_op_acc_by_number(644), acc2=get_op_acc_by_number(377), value=value) # 16 <-





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


# 377 «Расчеты с прочими дебиторами» - пассив
# 

# def test():
#     op_number_from = 
#     OperativeAccounts.objects.get(number=number)
#     AD_PC(100, 100)
#     AD_AC(5, 5)