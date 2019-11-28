import requests
import re
import copy
import random
import numpy as np
from decimal import Decimal as D

from calendar import monthrange
import datetime

from general_accounting.models import OperativeAccounts, AccountingBalance, TaxRate, TrialBalance
from django.contrib.auth.models import User

import unintegrated_features.task1.algs as algs

from mixins.models import Address
from company_operations.models import (Product, WareHouse, WHProduct, Purchase,
                                        perform_sale, SalaryPayment, 
                                        perform_Veh_repair_Payment, 
                                        perform_CommunalServisePayment, 
                                        get_next_date,
                                        Department, Fuel, Vehicle) # DemandForecastingReport 
from simulation.models import get_simulation
from simulation.up import import_to_hire_check#, perform_fire_checks
def populate_taxes():
    TaxRate.objects.get_or_create(name='for_Purchase', rate=0.2)
    TaxRate.objects.get_or_create(name='for_Sale', rate=0.2)
    TaxRate.objects.get_or_create(name='for_Salary', rate=0.18)
    TaxRate.objects.get_or_create(name='single_Tax', rate=0.05)
    TaxRate.objects.get_or_create(name='property_Tax', rate=0.015)

def get_accounts():
    link = 'https://dtkt.com.ua/documents/dovidnyk/plan_rah/plan-r.html'
    page = requests.get(link)
    regex = re.compile(r'(?<=<\/center>)(.*?)<\/tr>')
    page_html  = " ".join(((page.content).decode("cp1251")).split())
    from_center_to_td = (regex.search(page_html)).group(1)
    classification_regex = lambda d: re.compile(f'(?<=[^\d](\d{ {d} })[^\d])(.*?)[^<]*')
    accounts = {'1_level': {}, '2_level': {}, '3_level': {}}
    for reg in range(1, 4):
        sub_acc = {}
        for m in re.finditer(classification_regex(reg), from_center_to_td):
            sub_acc[f'{m.group(1)}'] = m.group(0)
        accounts[f'{reg}_level'] = copy.deepcopy(sub_acc)
    return accounts

def populate_OperativeAccounts(accs):
    for number, name in (accs['3_level']).items():
        OperativeAccounts.objects.create(name=name, classification=accs['1_level'][number[:1]], subclass=accs['2_level'][number[:2]], number=number)

def create_AB():
    AccountingBalance.objects.create()

def create_TB():
    TrialBalance.objects.create()

# def deikstra_choice():
#     algs.pre_dei(algs.read_apt_matrix(), {})
#     return algs.read_uprgated_routes()

# def floyd_choice():
#     algs.pre_flo(algs.read_apt_matrix(), {})
#     return algs.read_uprgated_routes()

# def get_upgrate_routes(func):
#     routes = globals()[func]() if func != 'dont_upgrade' else algs.read_uprgated_routes()

def get_binominal(ranges, prob):
    """ to first and second value of ids add  + 1"""
    return np.random.binomial(len(range(ranges[0], ranges[1])), prob) + ranges[0]

def get_float_binominal(ranges, prob):
    return float(get_binominal([int(ranges[0]*10), int(ranges[1]*10)], prob)/10)

def get_wh_addresses():
    for addr in algs.get_ph_addresses():
        yield addr.split(','), addr

def populate_wh_addresses():
    separator = ' /'
    addr_list = []
    for addr, init_addr in get_wh_addresses():
        addr_list.append(Address.objects.create(address_line=separator.join(addr[:-4]), city=addr[-4], region=addr[-3], country=addr[-2], postal_code=addr[-1], full_address=init_addr))
    return addr_list

def popualte_products(prod_num, markup_rate, cost_price):
    sim = get_simulation()
    product_list = []
    for product in range(prod_num):
        product_list.append(Product.objects.create(markup_rate=random.choice(np.arange(markup_rate[0], markup_rate[1], 0.01)), cost_price=get_float_binominal(cost_price, sim.product_cost_price_max_prob), name=f'name_#{product}', dozation=f'dozation_#{product}'))
    return product_list
def populate_wh():
    for ind, add in enumerate(populate_wh_addresses()):
        yield WareHouse.objects.create(address=add, pharmacy_number=ind)

def populate_whproducts(prod_num, markup_rate, cost_price, self_rate, whp_quantity, day_quantity_range, threshold_days):
    sim = get_simulation()
    whs = populate_wh()
    ps = popualte_products(prod_num, markup_rate, cost_price)
    for wh in whs:
        for product in ps:
            WHProduct.objects.create(self_rate=random.choice(np.arange(self_rate[0], self_rate[1], 0.1)), warehouse=wh, product=product, quantity=random.choice(range(whp_quantity[0], whp_quantity[1], 1)), threshold=sum((get_binominal(day_quantity_range, sim.d_q_r_max_prob) * (random.choice(np.arange(self_rate[0], self_rate[1], 0.1)))) for i in range(threshold_days)), threshold_days=threshold_days)

def create_one_department():
    Department.objects.create(organisation="Сеть Аптек 'Копейка'", address="Nezalezhnosti Blvd, 12, Brovary, Kyivs'ka oblast, Ukraine, 07400")

def populate_Fuel():
    Fuel.objects.create(fuel_price=28.73, fuel_type='A-95')
    Fuel.objects.create(fuel_price=27.00, fuel_type='А-92')
    Fuel.objects.create(fuel_price=27.80, fuel_type='ДТ')
    Fuel.objects.create(fuel_price=13.20, fuel_type='Газ')

def create_Vehicles(sim):
    [Vehicle.objects.create(vehicle_consumption=9.0, fuel=Fuel.objects.get(fuel_type='A-95'), vehicle_price=25000.0, vehicle_name='Ford Transit FT-190L', vehicle_full_address_now="Nezalezhnosti Blvd, 11, Brovary, Kyivs'ka oblast, Ukraine, 07400", for_transporting='Purchase') for i in range(sim.vehicles_purchase_num)]
    [Vehicle.objects.create(vehicle_consumption=9.0, fuel=Fuel.objects.get(fuel_type='A-95'), vehicle_price=25000.0, vehicle_name='Ford Transit FT-190L', vehicle_full_address_now="Nezalezhnosti Blvd, 11, Brovary, Kyivs'ka oblast, Ukraine, 07400", for_transporting='WHTransfer') for i in range(sim.vehicles_whtransfer_num)]

def gener_rand_bank_acc():
    bank_acc = [str(random.choice(range(0, 10))) for digit in range(16)]
    return ''.join(bank_acc)
    
def create_address(address):
    addr = address.split(',')
    separator = ' /'
    return Address.objects.create(address_line=separator.join(addr[:-4]), city=addr[-4], region=addr[-3], country=addr[-2], postal_code=addr[-1], full_address=address)

def create_vendor(sim):
    organisation, vendor_address = algs.get_distributor()
    created_v_a = create_address(vendor_address)     
    user = User.objects.create_user(username=f'vendor_{0}_{gener_rand_bank_acc()}', password=sim.that_user_password)
    user.refresh_from_db()
    user.profile.bank_acc = gener_rand_bank_acc()
    user.profile.save()
    user.profile.role_to_vendor(organisation=organisation, address=created_v_a)


def set_worker_role(kind, salary, address, number, sim, id):
    user = User.objects.create_user(username=f'worker_{kind}_{number}_{gener_rand_bank_acc()}', password=sim.that_user_password)
    user.refresh_from_db()
    user.profile.bank_acc = gener_rand_bank_acc()
    user.profile.save()

    # if kind in ('HR', 'accounting_manager', 'director', 'sys_admin'):
    #     work_on_dpt = Department.objects.all().last()
    # elif kind in ('pharmacist', 'cleaner'):

    # elif kind in ('loader', 'driver'):

    #     prob_of_worker_fired = sim.prob_of_worker_fired_hr
    #     work_on_dpt = apps.get_model('company_operations.Department').objects.all().last()
    # elif kind == 'accounting_manager':
    #     prob_of_worker_fired = sim.prob_of_worker_fired_am
    #     work_on_dpt = apps.get_model('company_operations.Department').objects.all().last()
    # elif kind == 'pharmacist':
    #     prob_of_worker_fired = sim.prob_of_worker_fired_ph
    #     work_on_wh = apps.get_model('company_operations.WareHouse').objects.all().last()
    # elif kind == 'director':
    #     prob_of_worker_fired = sim.prob_of_worker_fired_dir
    #     work_on_dpt = apps.get_model('company_operations.Department').objects.all().last()
    # elif kind == 'cleaner':
    #     prob_of_worker_fired = sim.prob_of_worker_fired_cl
    #     work_on_wh = apps.get_model('company_operations.WareHouse').objects.all().last()
    # elif kind == 'loader':
    #     prob_of_worker_fired = sim.prob_of_worker_fired_ld
    #     work_on_vehicle = apps.get_model('company_operations.Vehicle').objects.all().last()
    # elif kind == 'driver':
    #     prob_of_worker_fired = sim.prob_of_worker_fired_dr
    #     work_on_vehicle = apps.get_model('company_operations.Vehicle').objects.all().last()
    # elif kind == 'sys_admin':
    #     prob_of_worker_fired = sim.prob_of_worker_fired_sa
    #     work_on_dpt = apps.get_model('company_operations.Department').objects.all().last()

    user.profile.role_to_worker(kind=kind, salary=salary, address=address, id_workon_place=id)

def create_workers(sim):

    address_part = '_street, Some_house, Some_city, Some_city, Some_counrty, Some_postal_code'

    in_that_wh = sim.pharmacist_per_wh
    wh_id = WareHouse.objects.all().first().id # отсчет от первой аптеки ( если была перезагрузка (создание новой) модели симуляции)
    
    for index in range(sim.pharmacist_num):

        if in_that_wh > 0:
            in_that_wh -= 1
        else:
            in_that_wh = sim.pharmacist_per_wh
            wh_id += 1

        worker_address = f'Some_pharmacist#{index}{address_part}'
        created_w_a = create_address(worker_address)
        set_worker_role("pharmacist", sim.salary_pharmacist, created_w_a, index, sim, wh_id)

    dpt_id = Department.objects.all().first().id

    for index in range(sim.HR_num):
        worker_address = f'Some_HR#{index}{address_part}'
        created_w_a = create_address(worker_address)
        set_worker_role("HR", sim.salary_pharmacist, created_w_a, index, sim, dpt_id)

    for index in range(sim.accounting_manager_num):
        worker_address = f'Some_accounting_manager#{index}{address_part}'
        created_w_a = create_address(worker_address)
        set_worker_role("accounting_manager", sim.salary_accounting_manager, created_w_a, index, sim, dpt_id)

    in_that_wh = sim.cleaner_per_wh
    wh_id = WareHouse.objects.all().first().id
    
    for index in range(sim.cleaner_num):

        if in_that_wh > 0:
            in_that_wh -= 1
        else:
            in_that_wh = sim.cleaner_per_wh
            wh_id += 1

        worker_address = f'Some_cleaner#{index}{address_part}'
        created_w_a = create_address(worker_address)
        set_worker_role("cleaner", sim.salary_cleaner, created_w_a, index, sim, wh_id)

    in_that_veh = sim.loader_per_vehicle
    veh_id = Vehicle.objects.all().first().id

    for index in range(sim.loader_num):

        if in_that_veh > 0:
            in_that_veh -= 1
        else:
            in_that_veh = sim.loader_per_vehicle
            veh_id += 1

        worker_address = f'Some_loader#{index}{address_part}'
        created_w_a = create_address(worker_address)
        set_worker_role("loader", sim.salary_loader, created_w_a, index, sim, veh_id)

    in_that_veh = sim.driver_per_vehicle
    veh_id = Vehicle.objects.all().first().id
    
    for index in range(sim.driver_num):
        
        if in_that_veh > 0:
            in_that_veh -= 1
        else:
            in_that_veh = sim.driver_per_vehicle
            veh_id += 1

        worker_address = f'Some_driver#{index}{address_part}'
        created_w_a = create_address(worker_address)
        set_worker_role("driver", sim.salary_driver, created_w_a, index, sim, veh_id)

    for index in range(sim.sys_admin_num):
        worker_address = f'Some_sys_admin#{index}{address_part}'
        created_w_a = create_address(worker_address)
        set_worker_role("sys_admin", sim.salary_sys_admin, created_w_a, index, sim, dpt_id)

    worker_address = f'Some_Director{address_part}'
    created_w_a = create_address(worker_address)
    set_worker_role("director", sim.salary_director, created_w_a, 0, sim, dpt_id)

def create_clients(sim):
    for cl in range(sim.num_of_clients):
        user = User.objects.create_user(username=f'client_{cl}_{gener_rand_bank_acc()}', password=sim.that_user_password)
        user.refresh_from_db()
        user.profile.bank_acc = gener_rand_bank_acc()
        user.profile.save()

def populate_first_Purchses():
    for wh in WareHouse.objects.all():
        Purchase.objects.create(wh=wh)


# def populate_first_DemandForecastingReports():
#     that_month_day = datetime.date.today()
#     days_in_month = monthrange(that_month_day.year, that_month_day.month)[1]
#     day_to_report = that_month_day + datetime.timedelta(days_in_month)
#     for wh in WareHouse.objects.all():
#         DemandForecastingReport.objects.create(wh=wh, date_to_report=day_to_report)

def create_first_Veh_repair_Payment():
    perform_Veh_repair_Payment()

def create_first_CommunalServisePayment():
    perform_CommunalServisePayment()

def create_first_SalaryPayment():
    SalaryPayment.objects.create(date_to_pay=get_next_date())

def first_fire_check(sim):
    import_to_hire_check(sim, style=2)

def main(sim): # sim
    # sim = get_simulation()
    print('population populate_taxes ')
    populate_taxes()
    print('population populate_OperativeAccounts ')
    populate_OperativeAccounts(get_accounts())
    print('population create_AB ')
    create_AB()
    print('population create_TB ')
    create_TB()
    print('population populate_whproducts ')
    populate_whproducts(sim.number_of_products_names, sim.product_markup_rate, sim.product_cost_price, sim.whp_self_rate, sim.whp_quantity, sim.day_quantity_range, sim.threshold_days)
    print('population create_one_department ')
    create_one_department()
    print('population populate_Fuel ')
    populate_Fuel()
    print('population create_Vehicles ')
    create_Vehicles(sim)
    print('population create_vendor ')
    create_vendor(sim)
    print('population create_workers ')
    create_workers(sim)
    print('population create_clients ')
    create_clients(sim)
    print('population populate_first_Purchses ')
    populate_first_Purchses()
    # print('population populate_first_DemandForecastingReports ')
    # populate_first_DemandForecastingReports()
    print('population create_first_Veh_repair_Payment ')
    create_first_Veh_repair_Payment()
    print('population create_first_CommunalServisePayment ')
    create_first_CommunalServisePayment()
    print('population create_first_SalaryPayment ')
    create_first_SalaryPayment()
    print('population first_fire_check ')
    first_fire_check(sim)
    print('population ended ')

# main(sim)