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
import requests
from bs4 import BeautifulSoup
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

# def get_accounts():
#     link = 'https://dtkt.com.ua/documents/dovidnyk/plan_rah/plan-r.html'
#     first_tag = 'center'
#     second_tag = 'p'
#     third_tag = 'i'
#     fourth_tag = 'b'
#     page = requests.get(link)
#     if page.status_code == 200:
#         soup = BeautifulSoup(page.content, "html.parser")
#         # print(soup.find('center').text)
#         center_tag = soup.find(first_tag)
#         all_class = center_tag.find_next_siblings(second_tag, recursive=False) # find_all_next - сука циклится до без конца ( хз мож изз-за хуевого генератора)
#         classes = [one_class.findChild for one_class in all_class]# if one_class.next_element == third_tag]
#         print(classes)
#         # list(map(print, all_class))
#         # print(all_class)
#         # classes = [oneclass.text for oneclass in all_class if oneclass.findChild() == third_tag]
#         # subclasses = [subclass.text for subclass in classes if subclass.findChild() == fourth_tag]
#         # map(print, classes)
#         # map(print, subclasses)
#         # map(print, soup.find_next('center'))
#     else:
#         print('ERROR: \nCant load the page with Accounts numbers for general_accounting')
    

# def populate_OperativeAccounts(): 
#     OperativeAccounts.objects.create(name=, classification=, number=)



import requests
import re
import copy
import random
import numpy as np
from decimal import Decimal as D


from general_accounting.models import OperativeAccounts, AccountingBalance

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


import algs
import get_ph_data

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
    for addr in get_ph_data.get_addresses():
        yield addr.split(',')

# /\/\ should change to real names and dozens
# def get_products_names():
#       ...
#     # return names, dozens


from .models import Address
from company_operations.models import Product, WareHouse, WHProduct

def populate_wh_addresses():
    """ Так как первые 2 значения ардесов из гугл мапс могут быть либо улицей и домом или же просто 1 значение на какой-то участок, то
    берем отсчет сплита по коме от последнего елемента сплита"""
    separator = ' /' # -> "ulʹvar Oleksandriysʹkyy, 95" - >  "ulʹvar Oleksandriysʹkyy / 95"
    for addr in get_wh_addresses():
        yield Address.objects.create(address_line=separator.join(addr[:-4]), city=addr[-4], region=addr[-3], country=addr[-2], postal_code=addr[-1])

def popualte_products(prod_num, markup_rate, cost_price):
    """There we just randomly populate all fields of products"""
    for product in range(prod_num):
        yield Product.objects.create(
            # markup_rate=D(str(random.choice(np.arange(markup_rate[0], markup_rate[1], 0.01)))), # from float to decimal
            # cost_price=D(random.choice(range(cost_price[0], cost_price[1], 1))), 
            markup_rate=random.choice(np.arange(markup_rate[0], markup_rate[1], 0.01))
            cost_price=random.choice(np.arange(cost_price[0], cost_price[1], 0.1))
            name=f'name_#{product}', 
            dozation=f'dozation_#{product}')

def populate_wh():
    # every time after population the pharmacy_number can be changed
    for ind, add in enumerate(populate_wh_addresses()):
        yield WareHouse.objects.create(address=add, pharmacy_number=ind)

def populate_whproducts(prod_num, markup_rate, cost_price, whp_quantity):
    """ 
    # substituted by random day_quantity_range
    0.1 in step in random choice in np.arange of ranges 
    for self_rate cause of 
    WHProduct.self_rate = models.DecimalField(max_digits=2, decimal_places=1)
    """
    for wh in populate_wh():
        for product in popualte_products(prod_num, markup_rate, cost_price):
            WHProduct.objects.create(
                # self_rate=D(str(random.choice(np.arange(self_rate[0], self_rate[1], 0.1)))), 
                # substituted by random day_quantity_range
                self_rate=random.choice(np.arange(self_rate[0], self_rate[1], 0.1)), 
                warehouse=wh, 
                product=product, 
                quantity=random.choice(range(whp_quantity[0], whp_quantity[1], 1))
                )

def main():


    # created_first_simulation() 
    

    """
    day_quantity_range - для каждого продукта ежедневно (тоесть составляющая сейла) записывать в сейл 
    day_quantity_range - определяет рамки рандома при совершении сейла для каждого продукта в пре_сейл методе сигнале
    day_quantity_range - in model Sale as 2 fields: min_day_quantity max_day_quantity
    """
    choices = {#'sales_quantity_rate_ranges_per_day': [(0.015, 0.02), (0.02, 0.03), (0.03, 0.04), (0.04, 0.05)],
                'whp_self_rate': [(0.7, 1.5), (0.1, 5.0), (0.5, 2.0)],
                'day_quantity_range': [(2, 5), (3, 8), (5, 10)],
                'number_of_products_names': [100, 200, 300],
                'product_markup_rate': [(0.2, 0.3), (0.25, 0.3), (0.2, 0.25)],
                'product_cost_price': [(100.0, 1000.0), (200.0, 1000.0), (10.0, 1000.0)]
                'whp_quantity': [(50, 100), (50, 200), (100, 200)],
                }
    # populate_taxes()
    # populate_consts()
    # populate_OperativeAccounts()
    # get_accounts()
    populate_OperativeAccounts(get_accounts())
    create_AB()
    create_TB()
    populate_whproducts(prod_num=choices['number_of_products_names'][0], 
                        markup_rate=choices['product_markup_rate'][0],
                        cost_price=choices['product_cost_price'][0],
                        self_rate=choices['whp_self_rate'][0],
                        whp_quantity=choices['whp_quantity'][0])


main()

# /\/\ TODO change rangoms to binominal distribution