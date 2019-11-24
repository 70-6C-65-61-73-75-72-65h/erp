
# /\/\ TODO change rangoms to binominal distribution

# from django.contrib.auth.models import User
# from django.shortcuts import render, get_object_or_404, redirect
# import posts.models as posts_models #Post
# import likes.models as likes_models #Like
# import random

# import pickle

# def get_password_or_name(key='name'):
#     symb_to_choice = [[33, 35, 36, 37, 38, 42, 64, 94], 
#         list(range(48,58)), list(range(65, 91)), list(range(97, 123))] # # ==== !@#$%^&*  ///////// 33,126 
#     nums_to_choice = list(range(48,58)) # 0 - 9
#     upper_case_letters = list(range(65, 91))
#     lower__case_letters = list(range(97, 123))
#     all_symbols = sum(symb_to_choice, []) if key == 'password' else sum(symb_to_choice[1:], [])
#     gener_len = random.randint(8, 16) #  8-16 symbols in password
#     gener = []
#     for i in range(gener_len):
#         gener.append(random.choice(all_symbols)) # ascii symbols
#     gener = [chr(i) for i in gener]
#     return ''.join(gener)


# def dump_users(filename, data):
#     with open(filename, 'a') as f:
#         f.write(str(data))


# def populate_users(num):
#     filename =  r'_auto/users.txt'
#     user_data = [{'username': get_password_or_name(), 'password': get_password_or_name(key='password'), 'id': u} for u in range(2, num + 2)] # id = 1 for admin
#     dump_users(filename, user_data)
#     [User.objects.create_user(username = u['username'], password = u['password']) for u in user_data]
#     del user_data

# def get_post_user(num=None, id=None):
#     return User.objects.get(id=random.choice(range(2, num + 2))) if id is None else User.objects.get(id=id)

# def populate_posts(posts, users): # rand numof posts for each user    ###user=User.objects.get(username
#     for post in range(posts):
#         posts_models.Post.objects.create(title=f'title {get_password_or_name()}', content=f'content {get_password_or_name()}', owner=get_post_user(num=users)) # no image

# def populate_likes(likes, posts, users):  # rand numof likes for each post
#     # 2 likes at least or for latest posts 0 likes in likes if they are out of range
#     min_likes_per_post = likes / posts 
#     for post_id in range(1, posts + 1):
#         userset = set(range(2, users + 2))
#         # num of likes on post from min_likes_per_post to num of users or 0
#         for like in range(random.randint(min_likes_per_post, len(userset))): 
#             if likes == 0:
#                 del userset
#                 return None
#             post_like = likes_models.Like.objects.create(user=get_post_user(id=userset.pop()), post=posts_models.Post.objects.get(id=post_id))
#             # get_or_create return tuple (obj, True) while creating instance, while create return obj
#             # даже не проверяем на то что один и тот же юзер мог дважды пролукасить так как тут попом вытесняются повторяющиеся юзеры
#             # no vse zhe zachemto zapisali eto
#             post_like.value = 1
#             post_like.save()
#             likes -= 1
#         del userset


# def main(users, posts, likes):
#     print(f'populate {users} users')
#     populate_users(users)
#     print(f'populate {posts} posts')
#     populate_posts(posts, users)
#     print(f'populate {likes} likes')
#     populate_likes(likes, posts, users)
#     print('popoulation was ended')

# num_of_users = 20
# num_of_posts = 40
# num_of_likes = 80

# main(num_of_users, num_of_posts, num_of_likes)



# from accounts import TaxRate, CompanyConsts
# from general_accounting import OperativeAccounts
# import requests
# from bs4 import BeautifulSoup




# /\/\ all tax and company property info
# --------------------------------------------------------------------------------------------------------------------------------------------------------
# # HumanCapacity = Salary(per month)*KGoodwill 
# # Debit balance = HumanCapacity + Property + Money(in comp now)(in coffers)

# #  "общий доход" = (доход Sale - расход Purchase - расход EquipmentService(тут и автосервис, закупка и обновление оборудования в аптеках, департаменте, складах)  - расход на зарплаты) ) - если в плюс, то -> 18% на доход
# # если выручка по итогам предшествующих 12 месяцев превышает 1 млн грн. (это так для нашего предприятия) ->>>> + "НДС"  =  20% * ( "общий доход" - 1 млн ) 
# # "Единый налог" третья группа + 5% от  "общий доход"
# # "налог на недвижимость"  = (наугад взял цифру размер всех 138 аптек( по 40 кв м)==5520;  департамент=240 kv. m.;   ------
# # для гаражей – 0,01% за 1 квадратный метр базы ------ гаражи (20 машин)( по 12 кв м) == 240 )
# # № плата за землю  - нема ибо все и вся работает
# # "налог на авто" - представим что все авто старше 5 лет или стоимость каждой менее чем по 375 мин зп (375*4173) == 1 564 875‬ грн

# # итого:  ((доход Sale - расход Purchase - расход EquipmentService(тут и автосервис, закупка и обновление оборудования в аптеках, департаменте, складах)  - расход на зарплаты) ) * (18% + 5%)) 
# # Debit balance - денежная оценка стоимости имущества или имущественных прав предприятия (на данный момент времени ) (сейчас) 
# # --------------  все из проперти , + рабочие ( их оценочная стоимость (кадровый потенциал) ( в зависимости сколько они получают зп) и проф навыков и т.д.) + денежный
# # Debit turnover - денежная оценка !оперраций! приведшие к увеличению бабла в фирме  (за промежуток) (месяц) 
# # -------------- продажа товаров, доставка по аптекам, работа HR, форекастера, ...
# # # autametive insert values : 
# # min_salary : 4173
# # On_Company_Profit_tax : 18%
# # NDS_tax : 20%
# # Single_tax : 5%
# # On_Property_tax : 1.5% * min_salary * meters
# # On_Garage_tax : 0,01% * min_salary * meters
# # On_Auto_tax : 25000/12 в месяц # Ставка налога в годовом измерении составляет 25 тыс. грн за одну единицу автотранспорта
# # On_Salary_Profit_tax : 18%
# --------------------------------------------------------------------------------------------------------------------------------------------------------


# /\/\ TODO on not todo
# --------------------------------------------------------------------------------------------------------------------------------------------------------
# from general_accounting.models import TaxRate, CompanyConsts

# def populate_taxes():
#     tax_rates = {'Company_Profit': 0.18, 'Salary_Profit': 0.18, 'NDS': 0.2, 'Single': 0.05, 'Property': 0.05, 'Property': 0.0001}
#     [TaxRate.objects.create(name=tax_key, rate=tax_value) for tax_key, tax_value in tax_rates.items()]

# def populate_consts():
#     min_salary = 4173  # (hrn)
#     ###############
#     tax_auto = 25000 # (hrn)
#     limit_salaries_auto_cost = 375
#     num_auto = 20
#     # list of costs for each auto ( automaticly random of costs between 100k - 1mln) (100k ,110,...990, 1000k)
#     auto_costs = list(map(lambda: random.randrange(100000, 1000001, 10000), range(num_auto)))
#     ###############
#     num_garage = num_auto
#     # garage 12 - 20 meters
#     garage_meters = list(map(lambda: random.randrange(12, 21, 2), range(num_garage)))
#     ###############
#     num_pharmacies = 138
#     # pharmacy 25 - 50 meters
#     pharmacies_meters = list(map(lambda: random.randrange(25, 51, 1), range(num_pharmacies)))
#     ###############
#     num_department = 1
#     department_meters = list(map(lambda: random.randrange(300, 361, 10), range(num_department)))
#     ###############
#     num_warehouse = 3
#     warehouse_meters = list(map(lambda: random.randrange(400, 600, 10), range(num_warehouse)))

#     # population
#     CompanyConsts.objects.create(name='min_salary', value=str(min_salary))
#     CompanyConsts.objects.create(name='tax_auto', value=str(tax_auto))
#     CompanyConsts.objects.create(name='limit_salaries_auto_cost', value=str(limit_salaries_auto_cost))
#     CompanyConsts.objects.create(name='num_auto', value=str(num_auto))
#     CompanyConsts.objects.create(name='auto_costs', value=str(auto_costs))
#     CompanyConsts.objects.create(name='num_garage', value=str(num_garage))
#     CompanyConsts.objects.create(name='garage_meters', value=str(garage_meters))
#     CompanyConsts.objects.create(name='num_pharmacies', value=str(num_pharmacies))
#     CompanyConsts.objects.create(name='pharmacies_meters', value=str(pharmacies_meters))
#     CompanyConsts.objects.create(name='num_department', value=str(num_department))
#     CompanyConsts.objects.create(name='department_meters', value=str(department_meters))
#     CompanyConsts.objects.create(name='num_warehouse', value=str(num_warehouse))
#     CompanyConsts.objects.create(name='warehouse_meters', value=str(warehouse_meters))
#
# --------------------------------------------------------------------------------------------------------------------------------------------------------

import requests
import re
import copy
import random
import numpy as np
from decimal import Decimal as D


from general_accounting.models import OperativeAccounts, AccountingBalance, TaxRate


def populate_taxes():
    TaxRate.objects.create(name='for_Purchase', rate=0.2)
    TaxRate.objects.create(name='for_Sale', rate=0.2)
    TaxRate.objects.create(name='for_Salary', rate=0.18)
    TaxRate.objects.create(name='single_Tax', rate=0.05) # for all companies tax only 
    TaxRate.objects.create(name='property_Tax', rate=0.015)
    # от общего дохода при в КП 702 и в ДА 301 в 17 пункте = просто все от продаж(за месяц), 
    # - (селери за месяц) ДП 661 КА 301,  
    # - (коммуналка налог) ДП 377 КА 311
    # ( по сути просто сальдо на 301 счте ( по идее только + дебетовое сальдо может быть на активном счете))
    # нет --- а сальдо всех активов по дебету ! === dohod_za_period = (TrialBalance.end_saldo_credit - TrialBalance.start_saldo_debit)*TaxRate.single_Tax
def get_accounts():
    """ by index get value -> accounts['1_level']['1'] -> Необоротные активы """
    
    link = 'https://dtkt.com.ua/documents/dovidnyk/plan_rah/plan-r.html'
    page = requests.get(link)
    regex = re.compile(r'(?<=<\/center>)(.*?)<\/tr>')
    page_html  = " ".join(((page.content).decode("cp1251")).split())
    from_center_to_td = (regex.search(page_html)).group(1)
    classification_regex = lambda d: re.compile(f'(?<=[^\d](\d{ {d} })[^\d])(.*?)[^<]*')
    accounts = {'1_level': {}, '2_level': {}, '3_level': {}} #[:1]  # [:2] # full
    for reg in range(1, 4):
        sub_acc = {}
        for m in re.finditer(classification_regex(reg), from_center_to_td):
            sub_acc[f'{m.group(1)}'] = m.group(0) 
        accounts[f'{reg}_level'] = copy.deepcopy(sub_acc)
    return accounts

def populate_OperativeAccounts(accs):
    for number, name in accs['3_level'].itmes():
        OperativeAccounts.objects.create(name=name, 
                classification=accounts['1_level'][number[:1]], 
                subclass=accounts['2_level'][number[:2]], number=number)

def create_AB():
    AccountingBalance.objects.create()

def create_TB():
    TrialBalance.objects.create()


import unintegrated_features.task1.algs as algs
import unintegrated_features.task1.get_ph_data as get_ph_data

def deikstra_choice():
    algs.pre_dei(get_ph_data.read_apt_matrix(), {})
    return algs.read_uprgated_routes()

def floyd_choice():
    algs.pre_flo(get_ph_data.read_apt_matrix(), {})
    return algs.read_uprgated_routes()

# not called before - should call when the question of time of dispatch and delivery in (inventory tracking (when transfering self products (in quantity from one wh to another)))
# 'routing_alg': ["deikstra_choice", "floyd_choice", "dont_upgrade"],
def get_upgrate_routes(func):
    routes = globals()[func]() if func != 'dont_upgrade' else algs.read_uprgated_routes()

def get_wh_addresses():
    """Generator that returns an array of values for Address model (that for Warehouse models) populating"""
    for addr in get_ph_data.get_ph_addresses():
        yield addr.split(','), addr

# /\/\ should change to real names and dozens
# def get_products_names():
#       ...
#     # return names, dozens


from mixins.models import Address
from company_operations.models import (Product, WareHouse, WHProduct, 
                                        Purchase, perform_sale, 
                                        SalaryPayment, 
                                        perform_Veh_repair_Payment, perform_first_CommunalServisePayment, 
                                        get_next_date) #Sale, 

def populate_wh_addresses():
    """ Так как первые 2 значения ардесов из гугл мапс могут быть либо улицей и домом или же просто 1 значение на какой-то участок, то
    берем отсчет сплита по коме от последнего елемента сплита"""
    separator = ' /' # -> "ulʹvar Oleksandriysʹkyy, 95" - >  "ulʹvar Oleksandriysʹkyy / 95"
    for addr, init_addr in get_wh_addresses():
        yield Address.objects.create(address_line=separator.join(addr[:-4]), city=addr[-4], region=addr[-3], country=addr[-2], postal_code=addr[-1], full_address=init_addr)

def popualte_products(prod_num, markup_rate, cost_price):
    """There we just randomly populate all fields of products"""
    for product in range(prod_num):
        yield Product.objects.create(
            # markup_rate=D(str(random.choice(np.arange(markup_rate[0], markup_rate[1], 0.01)))), # from float to decimal
            # cost_price=D(random.choice(range(cost_price[0], cost_price[1], 1))), 
            markup_rate=random.choice(np.arange(markup_rate[0], markup_rate[1], 0.01)),
            cost_price=random.choice(np.arange(cost_price[0], cost_price[1], 0.1)),
            name=f'name_#{product}', 
            dozation=f'dozation_#{product}')

def populate_wh():
    # every time after population the pharmacy_number can be changed
    for ind, add in enumerate(populate_wh_addresses()):
        yield WareHouse.objects.create(address=add, pharmacy_number=ind)

def populate_whproducts(prod_num, markup_rate, cost_price, self_rate, whp_quantity, day_quantity_range, threshold_days):
    """ 
    # substituted by random day_quantity_range
    0.1 in step in random choice in np.arange of ranges 
    for self_rate cause of 
    WHProduct.self_rate = models.DecimalField(max_digits=2, decimal_places=1)
    """
    for wh in populate_wh():
        for product in popualte_products(prod_num, markup_rate, self_rate, cost_price):
            WHProduct.objects.create(
                # self_rate=D(str(random.choice(np.arange(self_rate[0], self_rate[1], 0.1)))), 
                # substituted by random day_quantity_range
                self_rate=random.choice(np.arange(self_rate[0], self_rate[1], 0.1)), 
                warehouse=wh, 
                product=product, 
                quantity=random.choice(range(whp_quantity[0], whp_quantity[1], 1)),
                threshold=sum(int(random.choice(range(day_quantity_range[0], day_quantity_range[1])) * (random.choice(np.arange(self_rate[0], self_rate[1], 0.1)))) for i in range(threshold_days)), # общее рандомное значение продаж за 7 дней на каждый продукт рандомно WHTransfer
                threshold_days=threshold_days,
                )

def create_one_department():
    """ used for CommunalServisePayment """
    Department.objects.create(organisation="Сеть Аптек 'Копейка'", address="Nezalezhnosti Blvd, 12, Brovary, Kyivs'ka oblast, Ukraine, 07400")

def populate_Fuel():
    Fuel.objects.create(fuel_price=28.73, fuel_type='A-95')
    Fuel.objects.create(fuel_price=27.00, fuel_type='А-92')
    Fuel.objects.create(fuel_price=27.80, fuel_type='ДТ')
    Fuel.objects.create(fuel_price=13.20, fuel_type='Газ')

def create_Vehicles():
    [Vehicle.objects.create(vehicle_consumption=9.0, fuel=Fuel.objects.get(fuel_type='A-95'), vehicle_price=25000.0, vehicle_name='Ford Transit FT-190L', vehicle_full_address_now="Nezalezhnosti Blvd, 11, Brovary, Kyivs'ka oblast, Ukraine, 07400") for i in range(vehicles_num)]

# populate models.accounts
def gener_rand_bank_acc(): # 16 digits
    # 48, 58 -> 0-9
    # bank_acc = [chr(random.choice(range(48, 58))) for digit in range(16)]
    # or
    bank_acc = [str(random.choice(range(0, 10))) for digit in range(16)]
    return ''.join(bank_acc)
    
def create_address(address):
    addr = address.split(',')
    return Address.objects.create(address_line=separator.join(addr[:-4]), city=addr[-4], region=addr[-3], country=addr[-2], postal_code=addr[-1], full_address=address)


def create_vendor():
    organisation, vendor_address = get_ph_data.get_distributor()
    addr = vendor_address.split(',')
    created_v_a = create_address(vendor_address)     
    # if not pre routed address - use max_days_on_delivery = 2
    user = User.objects.create(username=f'vendor_#{0}', password=get_simulation().that_user_password)
    user.refresh_from_db()
    user.profile.bank_acc = gener_rand_bank_acc()
    user.profile.save()
    user.profile.role_to_vendor(organisation=organisation, address=created_v_a)


def set_worker_role(kind, salary, address, number):
    user = User.objects.create(username=f'worker_{kind}#{number}', password=get_simulation().that_user_password)
    user.refresh_from_db()
    user.profile.bank_acc = gener_rand_bank_acc()
    user.profile.save()
    user.profile.role_to_worker(kind=kind, salary=salary, address=address)

def create_workers():
    sim = get_simulation()
    address_part = '_street, Some_house, Some_city, Some_city, Some_counrty, Some_postal_code'

    for index in range(sim.pharmacist_num):
        worker_address = f'Some_pharmacist#{index}{address_part}'
        created_w_a = create_address(worker_address)
        set_worker_role(kind="pharmacist", salary=sim.salary_pharmacist, created_w_a, index)

    for index in range(sim.HR_num):
        worker_address = f'Some_HR#{index}{address_part}'
        created_w_a = create_address(worker_address)
        set_worker_role(kind="HR", salary=sim.salary_pharmacist, created_w_a, index)

    for index in range(sim.accounting_manager_num):
        worker_address = f'Some_accounting_manager#{index}{address_part}'
        created_w_a = create_address(worker_address)
        set_worker_role(kind="accounting_manager", salary=sim.salary_accounting_manager, created_w_a, index)

    for index in range(sim.cleaner_num):
        worker_address = f'Some_cleaner#{index}{address_part}'
        created_w_a = create_address(worker_address)
        set_worker_role(kind="cleaner", salary=sim.salary_cleaner, created_w_a, index)

    for index in range(sim.loader_num):
        worker_address = f'Some_loader#{index}{address_part}'
        created_w_a = create_address(worker_address)
        set_worker_role(kind="loader", salary=sim.salary_loader, created_w_a, index)

    for index in range(sim.driver_num):
        worker_address = f'Some_driver#{index}{address_part}'
        created_w_a = create_address(worker_address)
        set_worker_role(kind="driver", salary=sim.salary_driver, created_w_a, index)

    for index in range(sim.sys_admin_num):
        worker_address = f'Some_sys_admin#{index}{address_part}'
        created_w_a = create_address(worker_address)
        set_worker_role(kind="sys_admin", salary=sim.salary_sys_admin, created_w_a, index)

    worker_address = f'Some_Director{address_part}'
    created_w_a = create_address(worker_address)
    set_worker_role(kind="director", salary=sim.salary_director, created_w_a, 0)



    # if not pre routed address - use max_days_on_delivery = 2


def create_clients(): # only for assesments
    for cl in range(get_simulation().num_of_clients):
        user = User.objects.create(username=f'client_#{cl}', password=get_simulation().that_user_password)
        user.refresh_from_db()
        user.profile.bank_acc = gener_rand_bank_acc()
        user.profile.save()


def populate_first_Purchses():
    for wh in WareHouse.objects.all():
        Purchase.objects.create(wh=wh)

def populate_first_DemandForecastingReports():
    for wh in WareHouse.objects.all():
        DemandForecastingReport.objects.create(wh=wh)

def create_first_Veh_repair_Payment():
    perform_Veh_repair_Payment()

def create_first_CommunalServisePayment():
    perform_first_CommunalServisePayment()

def create_first_SalaryPayment():
    SalaryPayment.objects.create(date_to_pay=get_next_date())

def main():


    # created_first_simulation() 
    sim = get_simulation()
    populate_taxes()
    """
    day_quantity_range - для каждого продукта ежедневно (тоесть составляющая сейла) записывать в сейл 
    day_quantity_range - определяет рамки рандома при совершении сейла для каждого продукта в пре_сейл методе сигнале
    day_quantity_range - in model Sale as 2 fields: min_day_quantity max_day_quantity
    """
    # choices = {#'sales_quantity_rate_ranges_per_day': [(0.015, 0.02), (0.02, 0.03), (0.03, 0.04), (0.04, 0.05)],
    #             'whp_self_rate': [(0.7, 1.5), (0.1, 5.0), (0.5, 2.0)],
    #             'day_quantity_range': [(2, 5), (3, 8), (5, 10)],  # min_day_quantity and max_day_quantity
    #             'number_of_products_names': [100, 200, 300],
    #             'product_markup_rate': [(0.2, 0.3), (0.25, 0.3), (0.2, 0.25)],
    #             'product_cost_price': [(100.0, 1000.0), (200.0, 1000.0), (10.0, 1000.0)],
    #             'whp_quantity': [(50, 100), (50, 200), (100, 200)],
    #             'threshold_days': [7] #  -за сколько дней до предположительного исчерпания продуктов надо делать заявку на закупку
    #             }

    populate_OperativeAccounts(get_accounts())
    create_AB()
    create_TB()
    populate_whproducts(sim.number_of_products_names, 
                        sim.product_markup_rate
                        sim.product_cost_price
                        sim.whp_self_rate
                        sim.whp_quantity
                        sim.day_quantity_range
                        sim.threshold_days
                        )

    create_one_department()
    populate_Fuel()
    create_Vehicles()

    create_vendor()
    create_workers()
    create_clinets()

    populate_first_Purchses() # before # to add to it claims before purchase_performed
    populate_first_DemandForecastingReports() # before

    create_first_Veh_repair_Payment() # before
    create_first_CommunalServisePayment() # before

    create_first_SalaryPayment() # after

main()

# /\/\ данные которые надо популить для дальнейшего взаимодействия с ними, если симуляция запустится