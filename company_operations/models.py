from django.db import models

from decimal import Decimal as D
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.contrib.postgres.fields import ArrayField

import random
import math
import datetime
from calendar import monthrange

from general_accounting.models import Assets, Passives, TaxRate
from accounts.models import Vendor, Worker #, Client  - при совершении поодиночного сейла SaleAlone
from simulation.models import get_simulation
from mixins.models import Address, MyDateField
# Create your models here.
from general_accounting import acc_operations
from .operations import forecast
# import unintegrated_features.task1.get_ph_data as get_ph_data
import unintegrated_features.task1.algs as alg

# before creating all of that should write (set)
# 1) a quantity of products (on each WareHouse) in WHProduct
# 2) other vals from accounts (written in comments)
# 3) random ranges to sales per day (which amount based on quantity of each product in each wh) -> WHProduct.quantity = 100 -> Sale.that_whproduct = random.
# 4) markup_rate for products (20-30)
# 5) changing all of datetimes fileds that get datefield = auto_now_add and auto_now to editable=true ( and in reciever before creation get simulaton time)

# а когда мне решать когда закупка?

# class Salary(models.Model):
#     # """ тут просто мы кучей учитывая зарплаты всех сотрудников совершаем зачисление зарплат"""
#     worker

# nachislit_salary()
#  /\/\after all them -> receiver create assets and passives with val


def get_next_date():
    that_month_day = get_simulation().today
    days_in_month = monthrange(that_month_day.year, that_month_day.month)[1]
    day_to_pay = that_month_day + datetime.timedelta(days_in_month)
    return day_to_pay
#__________________________________________________________________________________________________________
# from there for each WareHouse and 
class CommunalServisePayment(models.Model): # start month
    # """ тут просто мы кучей учитывая зарплаты всех сотрудников совершаем зачисление зарплат"""
    """ for each CommunalServise report about Payment """
    created = MyDateField(auto_now_add=True)
    next_payment = models.DateField()
    payment_value = models.FloatField()

def get_CommunalServisePayment_value(): # каждый месяц рандомно
    sim = get_simulation()
    minimal_zp = sim.minimal_zp
    pharmacys_sizes = sim.pharmacys_sizes
    department_size = sim.department_size
    tax_property_size_limit = sim.tax_property_size_limit
    pharmacys_spendingds = get_random_int(sim.pharmacys_spendingds)
    department_spendingds = get_random_int(sim.department_spendingds)
    warehouse_num = ast.literal_eval(CompanyConsts.objects.get(name="warehouse_num").value)

    get_property_tax = lambda size_meters: (size_meters - tax_property_size_limit) * TaxRate.objects.get(name='property_Tax').rate * minimal_zp if size_meters > tax_property_size_limit else 0
    payment_value = float(warehouse_num * (get_property_tax(pharmacys_sizes) + pharmacys_spendingds) +
                    Department.objects.all().count() * (get_property_tax(department_size) + department_spendingds))
    return payment_value

def perform_CommunalServisePayment(): # from _auto._up
    day_to_pay = get_next_date()
    payment_value = get_CommunalServisePayment_value()

    CommunalServisePayment.objects.create(next_payment=day_to_pay, payment_value=payment_value)

    acc_operations.communal_month_payment(value=payment_value)


def check_CommunalServisePayment(): # from simulation.up
    last_csp = CommunalServisePayment.objects.order_by("id").last()
    if last_csp.next_payment == get_simulation().today:
        perform_CommunalServisePayment()
#__________________________________________________________________________________________________________
#__________________________________________________________________________________________________________
class Veh_repair_Payment(models.Model): # start month
    created = MyDateField(auto_now_add=True)
    next_payment = models.DateField()
    payment_value = models.FloatField()

def get_Veh_repair_Payment_value(): # каждый месяц рандомно

    veh_repair_price_month = get_simulation().veh_repair_price_month
    vehicles_num = get_simulation().vehicles_num
    total_repair_value = 0
    for veh in range(vehicles_num):
        repair_for_veh = get_random_int(veh_repair_price_month)
        Vehicle.objects.get().update(veh_repair_price_month=repair_for_veh)
        total_repair_value += repair_for_veh

    return total_repair_value

def perform_Veh_repair_Payment(): # from _auto._up # при создании платим
    day_to_pay = get_next_date()
    payment_value = get_Veh_repair_Payment_value()

    Veh_repair_Payment.objects.create(next_payment=day_to_pay, payment_value=payment_value)

    acc_operations.vehicle_repair_spends_payment(value=payment_value)


def check_Veh_repair_Payment(): # from simulation.up
    last_vrp = Veh_repair_Payment.objects.order_by("id").last()
    if last_vrp.next_payment == get_simulation().today:
        perform_Veh_repair_Payment()

#__________________________________________________________________________________________________________
# @receiver(post_save, sender=CommunalServisePayment):
# def CommunalServisePayment_set_A_P(sender, instance, created, **kwargs):
#     if created:
#         acc_operations. ( )

#__________________________________________________________________________________________________________
# from accounts
class SalaryPayment(models.Model): # end month
    """ for each worker report about payment """
    # worker = models.ForeignKey(Worker, related_name='salary_payments', on_delete=models.SET_NULL) # send_salary(worker.profile.bank_acc)   worker.salary           send_money_to_vendor(vendor.profile.bank_acc)
    created = MyDateField(auto_now_add=True)
    payment_value = models.FloatField(default=0.0)
    date_to_pay = models.DateField()


def get_SalaryPayment_value():
    # sim = get_simulation()
    total_value = sum(worker.salary for worker in Worker.objects.all())
    # total_value = sim.salary_pharmacist * sim.pharmacist_num +
    #                 sim.salary_HR * sim.HR_num +
    #                 sim.salary_accounting_manager * sim.accounting_manager_num +
    #                 sim.salary_cleaner * sim.cleaner_num +
    #                 sim.salary_loader * sim.loader_num +
    #                 sim.salary_driver * sim.driver_num +
    #                 sim.salary_sys_admin * sim.sys_admin_num +
    #                 sim.salary_director
    return total_value

def permorm_SalaryPayment(last_sp): # по окончанию срока платим
    day_to_pay = get_next_date()
    payment_value = get_SalaryPayment_value() # total value of all salaries that was payed

    last_sp.payment_value = payment_value # добавить в давно созданую модель значения уплаты и потом вызов активов пассивов а потом создать новую модель по уплате
    last_sp.save()

    acc_operations.salary_payment(payment_value)

    SalaryPayment.objects.create(date_to_pay=day_to_pay)

def check_SalaryPayment(): # from simulation.up
    last_sp = SalaryPayment.objects.order_by("id").last()
    if last_sp.date_to_pay == get_simulation().today:
        permorm_SalaryPayment(last_sp)
#__________________________________________________________________________________________________________

# на каждую аптеку пурчейз отдельно
class Purchase(models.Model):  # when needed                                                       # 1 на все закупки у вендора в соответствии с клеймами
    """
    Our purchases from vendor 
    (where vendor is a person that dealed with us) 
    so we import its model from accounts.models
    """
    tax = models.ForeignKey(TaxRate, related_name='purchases', on_delete=models.CASCADE)
    vendor = models.ForeignKey(Vendor, related_name='purchases', on_delete=models.CASCADE)

    in_queue = models.BooleanField(default=False) # ожидает свободную машину для поездки к вендору на закупку
    started = models.BooleanField(default=False)
    performed = models.BooleanField(default=False)
    
    wh = models.ForeignKey("WareHouse", related_name='purchases', on_delete=models.CASCADE) # setting while creating потому что надо не потерятся какой Purchase заменять, с какой аптекой
    
    # whtransfer = models.ForeignKey("WHTransfer", related_name='purchases', on_delete=models.CASCADE) # хочу сделать Purchase как WHTransfer

    arrival_time = models.DateTimeField(blank=True)
    way_costs = models.FloatField(default=0.0)
    used_vehicle_id = models.IntegerField(max_length=3, blank=True)

    arrival_to_start = models.DateTimeField(blank=True)

    total_price = models.FloatField(default=0.0)
    total_markup_price = models.FloatField(default=0.0)
    
    demanded = ArrayField(models.IntegerField(max_length=10), blank=True) #if not instance.demanded

    # а вот если паралельно с закупками куча трансферов меж продуктами будет, то бом-бом бошке)
    def perform_purchase(self):
        if Vehicle.objects.filter(used_now=False).exists():
            self.start_purchase(Vehicle.objects.filter(used_now=False)[0])
        else:
            self.in_queue = True # очередь мож длится долго, ибо кто первый схватил машину на пурчейз тот и король 
            # but after that we anyway create a new Purchase to that wh to add next claims to it


    def start_purchase(self, vehicle):

        self.used_vehicle_id = vehicle.id
        vehicle.used_now = True

        from_vehicle_addr = vehicle.vehicle_full_address_now # здесь он был до поездки


        start_addr = (Vendor.objects.all().last()).address.full_address
        end_addr = self.wh.address.full_address

        vehicle.go_from_addr = from_vehicle_addr
        vehicle.go_to_addr = start_addr

        vehicle.save()

        # in hours
        pre_spended_hours = ((get_ph_data.get_route_time_to_wh(from_vehicle_addr, start_addr))/60/60)* get_simulation().delivery_added_time_koef
        spended_hours = ((get_ph_data.get_route_time_to_wh(start_addr, end_addr))/60/60)* get_simulation().delivery_added_time_koef #* get_simulation().delivery_added_time_koef * get_simulation().num_of_phs_on_1_vehicle # 0.4*1.15*11
        
        self.arrival_time = get_simulation().today_time + datetime.timedelta(hours=(pre_spended_hours + spended_hours))
        self.arrival_to_start = get_simulation().today_time + datetime.timedelta(hours=(pre_spended_hours))

        self.way_costs = (get_ph_data.get_route_distance_to_wh(from_vehicle_addr, start_addr) / 100000) * get_simulation().vehicle_consumption * get_simulation().fuel_price +
                        (get_ph_data.get_route_distance_to_wh(start_addr, end_addr) / 100000) * get_simulation().vehicle_consumption * get_simulation().fuel_price

        pcs = self.purchase_claims.all() # markup_price
        self.total_price = sum(pc.whp.product.cost_price * pc.quantity for pc in pcs)
        self.total_markup_price = sum(pc.whp.product.markup_price * pc.quantity for pc in pcs)
        # for pc in pcs: #quantity whp
        #     whp1 = pc.whp

            # whp1 = WHProduct.objects.get(product=pc.whp.product, warehouse=pc.whp.warehouse)
        # whtcs = WHTransferClaim.objects.filter(from_wh=self.from_wh, to_wh=self.to_wh, accepted=True, started=False, performed=False, created__gte=self.expired_whtcs()) # не успеют заново запросится пока эти не исполнятся, 
        # for whtc in whtcs:
        #     whp1 = WHProduct.objects.get(product=whtc.product, warehouse=whtc.from_wh)
        #     whp1.quantity -= whtc.quantity
        #     whp1.save()
        #     whtc.started = True
        #     whtc.save()

        self.started = True
        self.save()


    def vehicle_arrived_to_start(self):
        """ checks every hour """
        # if self.arrival_to_start == get_simulation().today_time:
        vehicle = Vehicle.objects.get(id=used_vehicle_id)
        vehicle.transfering = True
        start_addr = self.from_wh.address.full_address
        end_addr = self.to_wh.address.full_address
        vehicle.go_from_addr = start_addr
        vehicle.go_to_addr = end_addr

        # vehicle.vehicle_full_address_now  - остается начальным отправным, во время всей поездки
        # vehicle.vehicle_full_address_now = 'unrecognized' #(cause in transfer now) -----------
        vehicle.save()

    def end_purchase(self):
        vehicle = Vehicle.objects.get(id=self.used_vehicle_id)
        vehicle.vehicle_full_address_now = vehicle.go_to_addr
        vehicle.used_now = False
        vehicle.transfering = False
        vehicle.save()

        # whtcs = self.WHTransferClaims.filter(accepted=True)
        # тут уже назад нт смысла отправлять, ибо доставили, потому expired_whtcs() не используется
        # whtcs = WHTransferClaim.objects.filter(from_wh=self.from_wh, to_wh=self.to_wh, accepted=True, started=True, performed=False) # , created__gte=self.expired_whtcs())
        # for whtc in whtcs:
        #     whp2 = WHProduct.objects.get(product=whtc.product, warehouse=whtc.to_wh)
        #     whp2.quantity += whtc.quantity
        #     whp2.save()
        #     whtc.performed = True
        #     whtc.save()
        pcs = self.purchase_claims.all()
        for pc in pcs:
            pc.whp.quantity += pc.quantity
            pc.save()

        self.performed = True
        self.save()
    
    # purchase_claims

    # def start_purchase(self):
    #     purchase_claims.all()
    #     self.started = True
    #     self.save()

    # def end_purchase(self):
    #     self.ended = True
    #     self.save()

@receiver(pre_save, sender=Purchase)
def set_Purchase_vals(sender, instance, *args, **kwargs):
    if not instance.vendor:
        instance.vendor = Vendor.objects.all().last()
        instance.tax = TaxRate.objects.get(name='for_Purchase')
        instance.save()


@receiver(post_save, sender=Purchase)
def Purchase_set_A_P(sender, instance, created, **kwargs):
    if instance.started == True and instance.performed == False: # if already perform and then save do accounting operations
        acc_operations.fuel_spends_payment(instance.way_costs)
        # оплатили продукты
        acc_operations.payment_to_suppliers_for_all(instance.total_price)
        # we create new Purchase to be added to new upcoming PurchaseClaims
        Purchase.objects.create(wh=instance.wh)
    elif instance.started == False and instance.performed == False:
        # запускаем процесс
        instance.perform_purchase()
    elif instance.started == True and instance.performed == True:
        # получаем продукты
        acc_operations.received_products(instance.total_markup_price)

    instance.save()


# def @receiver

# @receiver(post_save, sender=Purchase)
# def Purchase_set_A_P(sender, instance, created, **kwargs):
#     if created:
#         all_whps_claims = instance.purchase_claims.all()
#         to_payment = sum([whp_claim.whp.product.cost_price * whp_claim.quantity for whp_claim in all_whps_claims])
#         to_products = sum([whp_claim.whp.product.markup_price  * whp_claim.quantity for whp_claim in all_whps_claims])
#         # all_whps.product.cost_price #  zaplatit
#         # all_whps.product.markup_price # nazenit i dobavit d actives

#         acc_operations.received_products(value=to_payment)
#         acc_operations.payment_to_suppliers_for_all(value=to_products)

#         for whp_claim in all_whps_claims:
#             whp_claim.whp.quantity += whp_claim.quantity
#             whp_claim.claim_executed = True
#             # save product with updated quantity
#             whp_claim.whp.save()
#             # sale claim with status finished
#             whp_claim.save()

    # there we store products and their quantity to buy # if first and no DemandForecasting rows in table -> use standart baesd on 
    # demanded =





#receiver post to (by acc_operations.py) ass and pass  


# нужен процес проверки на expire_day в PurchaseClaim
# PurchaseClaim по 1 whp - потому куча продуктов собирается в Purchase
class PurchaseClaim(models.Model): # when needed                               # это именно там где менее порога или закончилось (до 4500 мож быть кст тоже)
    # /\/\ automate increasing days to 1)decrease days_to_expire and to 2)change all DateField(editable=True) faster than day will came
    # days_to_expire = models.IntegerField(max_length=1)
    """
        expire_day and max_days_on_delivery in set_PurchaseClaim_expire_day()
        quantity and whp in transfer_products()
        claim_executed - settled after PC is expire and executed in perform_purchase()
    """
    expire_day = models.DateField() # auto_now_add = created simulation day  # auto_now = updated simulation day # to add value and edit it every simulation day
    quantity - models.IntegerField(max_length=5)
    whp = models.ForeignKey('WHProduct', related_name='purchase_claims', on_delete=models.CASCADE)
    # claim_executed = models.BooleanField(default=False) # already_ordered and not gonna searched in future to purchase 
    max_days_on_delivery = models.IntegerField(default=2) # /\/\ определять по значениям из роутов * 2 ( как задержка ) # ofc найбольшое время по доставке 2 дня - потолок \\ ибо потолок реального секономленного времени - пол дня
    
    purchase = models.ForeignKey(Purchase, related_name='purchase_claims', on_delete=models.CASCADE)

# /\/\ rewrite
@receiver(pre_save, sender=PurchaseClaim)
def set_PurchaseClaim_expire_day(sender, instance, *args, **kwargs):
    # if quantity is settled -> Sale already is performed
    if not instance.purchase: #instance.expire_day and not instance.purchase:

        # выберем 4 самых длинный путей от вендора до аптек, для определениия наихудщего случая
        first_Pharmacies = algs.read_routes_from_vendor_duration_descending()[:get_simulation().num_of_phs_on_1_vehicle] # 4

        # выбираем наугад любую манишу и берем ее начльный адрес , только лишь для расчета доп времени по расстоянию для 
        # прибытия в начальный адрес (первый адрес с максимально долгой доставкой)
        veh_start_addr = Vehicle.objects.all().last().vehicle_full_address_now  # "Kapushanska St, 19, Uzhhorod, Zakarpats'ka oblast, Ukraine, 88000"
        vendor_addr = (Vendor.objects.all().last()).address.full_address # "Bulʹvar Oleksandriysʹkyy, 95, Bila Tserkva, Kyivs'ka oblast, Ukraine, 09100"
        # ЦЕПЬ
        # from start_vehicle_addr to vendor_addr -> 
        # from vendor_addr to max_delivery_time_addrs[0] -> 
        # from max_delivery_time_addrs[0] to vendor_addr -> 
        # from vendor_addr  to max_delivery_time_addrs[1] ....
        all_time = []
        all_time.append(algs.get_route_time_to_wh(veh_start_addr, vendor_addr))
        for i in first_Pharmacies:
            all_time.append(i[0]["duration"]) # from vend
            all_time.append(i[0]["duration"]) # to vend

        max_days_on_delivery = math.ceil((sum(all_time) * get_simulation().delivery_added_time_koef)/60/60/24)
        # print((sum(all_time)/60/60/24)*1.15) #  - 15% -  это доп время при доставке , все это в секундах
        del all_time
        instance.max_days_on_delivery = max_days_on_delivery
        instance.expire_day =  get_simulation().today + datetime.timedelta(days=(instance.wph.threshold_days - max_days_on_delivery))

        # wh_addr = instance.whp.warehouse.address.full_address
        # self_wh = instance.whp.warehouse
        # пока  не произведена закупка старых товаров по PurchaseClaim ак как они в очереди на исполнение, - 
        # не считаем стоимость всех товаров и не шлем в бухучет 
        # и не считаем затраты на топливо и не шлем бухучет
        # !!! считаем товары после started=True, тогда же и создаем новую пурчейзу к которой уже будут добавлятся новые PurchaseClaim в этой аптеке
        instance.purchase = Purchase.objects.get(wh=instance.whp.warehouse, performed=False, started=False)#, in_queue=False)

        instance.save()



# once in a day
def check_on_start_purchases():
    for p in Purchase.objects.filter(performed=False, started=False, in_queue=False):
        if p.purchase_claims.all().exists():
            if p.purchase_claims.filter(expire_day=get_simulation().today).exists():
                p.perform_purchase()

# ежечасово проверяем на доступ к тачке шоб сделать perform_purchase который острочивается в in_queue
# def check_purchase_delivery_queue(today_time):
#     for p in Purchase.objects.filter(performed=False, started=False, in_queue=True).exists():


def check_purchase_arrival(today_time): # to start perform new transfers that can be started cause of vehicles lack 
    # if arrived to wh
    if Purchase.objects.filter(arrival_time=today_time).exists(): #  -  по сути проверяет arrival_time предыдущего WHTransfer - потом освобождает тачки - и их можно использывать в след стейтменте
        [p.end_purchase() for p in Purchase.objects.filter(arrival_time=today_time)]

    # if not started cause of vehicle lack and check on ability to start 
    if Purchase.objects.filter(performed=False, started=False, in_queue=True).exists(): # cause if i create 
        [p.perform_purchase() for p in Purchase.objects.filter(performed=False, started=False, in_queue=True)]

    # if vehicle on start position to transfer product
    if Purchase.objects.filter(arrival_to_start=today_time).exists():
        [p.vehicle_arrived_to_start() for p in Purchase.objects.filter(arrival_to_start=today_time)]


# vendor = start_address = "Bulʹvar Oleksandriysʹkyy, 95, Bila Tserkva, Kyivs'ka oblast, Ukraine, 09100"
# get_route_time_to_wh(whp1.warehouse.address.full_address, whp2.warehouse.address.full_address)
#  у нас реализовано только под 1 вендора, так как есть только 1 адрес вендора
# get_route_vendor_to_wh((Vendor.objects.all().last()).address.full_address, whp.warehouse.address.full_address)
# after all sales per day

# from Purchase
# class WHPurchaseTransfer(models.Model):
#     # надо расчитать какая из доставок будет раньше другой для определенного колличества авто в запасе ( 4 ) (44)
#     # тут без клеймов, сразу с пурчейза посылка на трансфер меж вендоом и аптеками
#     max_days_on_delivery = math.ceil(((get_route_time_to_wh(vendor_addr, wh_addr) * delivery_added_time_koef)/60/60/24) * num_of_phs_on_1_vehicle)




# self.WHTransferClaims.all()
# self.purchases.all()
#  1 таблица сразу меж всеми аптеками и меж вендором и аптеками
# and for purchase too!!!!!
# просто пересылка без указания колличества, все значения по количеству в клеймах, которе тут кст изменяется путем захвата тех клеймов что к этому трансферу отнесены не напрямую а через поля
class WHTransfer(models.Model):  # when needed                   # по 1 на отрасление меж аптеками # сразу все трансферы тут с разных аптек
    # тоесть если мы отправили с 1 аптеки сразу в несколько других
    # так как аптеки все в разных городах то смысл отправлять в другую аптеку далеко есть только если продуктов из 1 в 2 отправляется более (задать) 300 в квонтити колличестве тоесть маловероятно
    # from_wh_to_others_time_days = models.IntegerField(max_length=5) # считаем в math.ceil(get_ph_data * 2 ) 
    # arrival_day = models.DateField(blank=True)
    # way_costs = models.FloatField(default=0.0)
    # started = models.BooleanField(default=False)
    # ended = models.BooleanField(default=False)

    # from_wh = # or vendor 
    # to_wh =
    # quantity =
    # accepted = models.BooleanField(default=False)

    from_wh = models.ForeignKey('WareHouse', related_name='WHTransfers', on_delete=models.CASCADE) 
    to_wh = models.ForeignKey('WareHouse', related_name='WHTransfers', on_delete=models.CASCADE)

    started = models.BooleanField(default=False)
    ended = models.BooleanField(default=False)

    arrival_time = models.DateTimeField(blank=True)
    way_costs = models.FloatField(default=0.0)
    used_vehicle_id = models.IntegerField(max_length=3, blank=True)

    arrival_to_start = models.DateTimeField(blank=True)

    def expired_whtcs(self):
        return get_simulation().today - datetime.timedelta(days=get_simulation().threshold_days)

    def perform_WHT(self):
        if Vehicle.objects.filter(used_now=False).exists():
            self.start_transfer(Vehicle.objects.filter(used_now=False)[0])
        #     return True
        # else:
        #     return False

    def start_transfer(self, vehicle):
        self.used_vehicle_id = vehicle.id
        vehicle.used_now = True

        from_vehicle_addr = vehicle.vehicle_full_address_now # здесь он был до поездки

        start_addr = self.from_wh.address.full_address
        end_addr = self.to_wh.address.full_address

        vehicle.go_from_addr = from_vehicle_addr
        vehicle.go_to_addr = start_addr
        # vehicle.transfering = False

        vehicle.save()
        # in hours
        pre_spended_hours = ((get_ph_data.get_route_time_to_wh(from_vehicle_addr, start_addr))/60/60)* get_simulation().delivery_added_time_koef
        spended_hours = ((get_ph_data.get_route_time_to_wh(start_addr, end_addr))/60/60)* get_simulation().delivery_added_time_koef #* get_simulation().delivery_added_time_koef * get_simulation().num_of_phs_on_1_vehicle # 0.4*1.15*11
        
        self.arrival_time = get_simulation().today_time + datetime.timedelta(hours=(pre_spended_hours + spended_hours))
        self.arrival_to_start = get_simulation().today_time + datetime.timedelta(hours=(pre_spended_hours))

        self.way_costs = (get_ph_data.get_route_distance_to_wh(from_vehicle_addr, start_addr) / 100000) * get_simulation().vehicle_consumption * get_simulation().fuel_price +
                        (get_ph_data.get_route_distance_to_wh(start_addr, end_addr) / 100000) * get_simulation().vehicle_consumption * get_simulation().fuel_price

        
        # whtcs = self.WHTransferClaims.filter(accepted=True)
        # whtcs = self.WHTransferClaims.all()
        # за 7 дней до этого WHTransfer исполнения были созданы - то мы их отсекаем ( даже если это были изначально и для этого WHTransfer созданы - все равно они уже пополнились через PurchaseClaim)
        # if created >= expired_whtcs - истекло
        whtcs = WHTransferClaim.objects.filter(from_wh=self.from_wh, to_wh=self.to_wh, accepted=True, started=False, performed=False, created__gte=self.expired_whtcs()) # не успеют заново запросится пока эти не исполнятся, 
        for whtc in whtcs:
            whp1 = WHProduct.objects.get(product=whtc.product, warehouse=whtc.from_wh)
            whp1.quantity -= whtc.quantity
            whp1.save()
            whtc.started = True
            whtc.save()

        self.started = True
        self.save()

    def vehicle_arrived_to_start(self):
        """ checks every hour """
        # if self.arrival_to_start == get_simulation().today_time:
        vehicle = Vehicle.objects.get(id=used_vehicle_id)
        vehicle.transfering = True
        start_addr = self.from_wh.address.full_address
        end_addr = self.to_wh.address.full_address
        vehicle.go_from_addr = start_addr
        vehicle.go_to_addr = end_addr

        # vehicle.vehicle_full_address_now  - остается начальным отправным, во время всей поездки
        # vehicle.vehicle_full_address_now = 'unrecognized' #(cause in transfer now) -----------
        vehicle.save()

    def end_transfer(self):
        vehicle = Vehicle.objects.get(id=self.used_vehicle_id)
        vehicle.vehicle_full_address_now = vehicle.go_to_addr
        vehicle.used_now = False
        vehicle.transfering = False
        vehicle.save()

        # whtcs = self.WHTransferClaims.filter(accepted=True)
        # тут уже назад нт смысла отправлять, ибо доставили, потому expired_whtcs() не используется
        whtcs = WHTransferClaim.objects.filter(from_wh=self.from_wh, to_wh=self.to_wh, accepted=True, started=True, performed=False) # , created__gte=self.expired_whtcs())
        for whtc in whtcs:
            whp2 = WHProduct.objects.get(product=whtc.product, warehouse=whtc.to_wh)
            whp2.quantity += whtc.quantity
            whp2.save()
            whtc.performed = True
            whtc.save()

        self.ended = True
        self.save()
        
# если создали WHTransfer, но еще не начался процессы пересылки - instance.perform_WHT() - начало процесса пересылки
#  1 раз это проходим, но потом в check_WHT_arrival проверям ежечасово чтоб запустить трансфер
@receiver(post_save, sender=WHTransfer)
def WHTransfer_set_A_P(sender, instance, created, **kwargs):
    if instance.started == True and instance.end == False: # if already perform and then save do accounting operations
        acc_operations.fuel_spends_payment(instance.way_costs)
        WHTransfer.objects.create()
    elif instance.started == False and instance.end == False:
        instance.perform_WHT()
    instance.save()
    
# only from simulation # from simulation.up.check_WHT_transfer() or from perform_sale()
def check_WHT_arrival(today_time): # to start perform new transfers that can be started cause of vehicles lack 
    if WHTransfer.objects.filter(arrival_time=today_time).exists(): #  -  по сути проверяет arrival_time предыдущего WHTransfer - потом освобождает тачки - и их можно использывать в след стейтменте
        [wht.end_transfer() for wht in WHTransfer.objects.filter(arrival_time=today_time)]

    if WHTransfer.objects.filter(started=False).exists(): # cause if i create 
        [wht.perform_WHT() for wht in WHTransfer.objects.filter(started=False)]

    if WHTransfer.objects.filter(arrival_to_start=today_time).exists():
        [wht.vehicle_arrived_to_start() for wht in WHTransfer.objects.filter(arrival_to_start=today_time)]
    
# def clean_WHTransferClaims(models.Model):
#     threshold_days
# WHTransferClaim могут оформится и кучей продуктов с 1 к другой аптеке - следовательно - 

# ; просто за стуки собираем по всем продуктам клеймы и пушим это в WHTransfer изи ( там будет просто from_wh_to_wh_time_days ) ( по сути не может быть больше чем роутов)
class WHTransferClaim(models.Model):                # експаир тут не будет, тут будет сразу отправка на пересылку меж аптеками, если найдено лишнее у других
    """ for each whp can claim """
    # чистить WHTransferClaim будем, но чтоб не удалить whp -  on_delete=models.SET_NULL
    from_wh = models.ForeignKey('WareHouse', related_name='WHTransferClaims', on_delete=models.SET_NULL)
    to_wh = models.ForeignKey('WareHouse', related_name='WHTransferClaims', on_delete=models.SET_NULL)
    product = models.ForeignKey('Product', related_name='WHTransferClaims', on_delete=models.SET_NULL)
    # whtransfer = models.ForeignKey(WHTransfer, related_name='WHTransferClaims', on_delete=models.CASCADE)
    quantity = models.IntegerField(max_length=10)
    accepted = models.BooleanField(default=False)
    started = models.BooleanField(default=False)
    performed = models.BooleanField(default=False)
    created = MyDateField(auto_now_add=True)
    


# def perform_Purchase(): #every day, so we cant miss expire_day
#     today = get_simulation().today # simulation today
#     if PurchaseClaim.objects.filter(claim_executed=False, expire_day=today).exists():
#         whp_to_buy = PurchaseClaim.objects.filter(claim_executed=False)
#         purchase = Purchase.objects.create(  )
        # purchase.purchase_claims_to_buy.add()
        # /\/\ best foo = Foo()
                    # foo.save()
                    # foo.bars.add(1,2)
        # purchase_claim_to_buy


# Бензин А-95 - price_fuel=28.73 - https://biz.liga.net/tek/oil/a-95
# 48,7 л: 517 км х 100 = 9,4 л / 100 км
# # distance # "указать" расход  9,4 л / 100 км  -> расход_топлива_за_поездку = 9,4 л  * distance / 100 000 -> расход_топлива_за_поездку*price_fuel
# http://www.1gai.ru/baza-znaniy/vajno-znat/520539-kalkulyator-rashoda-topliva-rasschitat-rashod-topliva.html

# # calc arrival_day way_costs ?/\/\
# def perform_WHTransfer(whs, fuel_price, vehicle_consumption): # 300  \\ 28.73 \\  9.4
    
    
#     # if for all in time 
    
    
    
#     all_whs_id = [wh.id for wh in whs] #[wh.id for wh in WareHouse.objects.all()]
#     arrival_day_s = []
#     way_costs_s = []
#     list_of_transfers = [] # {"arrival_day": , "way_costs": , "from_wh":, "to_wh":, "product":,}
#     for wh1_id in all_whs_id:
#         for wh2_id in all_whs_id:
#             whtcs = WHTransferClaim.objects.filter(from_wh__id=wh1_id, to_wh__id=wh2_id)
#             if sum([whtc.quantity for whtc in whtcs]) >= get_simulation().number_to_dispatch:# ( from 1 ph  to a lot of others )
#                 start_addr = WareHouse.objects.get(id=wh1_id).address.full_address
#                 end_addr = WareHouse.objects.get(id=wh1_id).address.full_address
#                 #       get_simulation().vehicles_num < get_simulation().warehouse_num, то мы домножаем
#                 #       но при пурчейзовском трансфере тоже домножаем, но там будет больше аптек, а знач и доставка будет дольше
#                 spended_days = ((get_ph_data.get_route_time_to_wh(start_addr, end_addr))/60/60/24)* #* get_simulation().delivery_added_time_koef * get_simulation().num_of_phs_on_1_vehicle # 0.4*1.15*11

#                 arrival_day = get_simulation().today + datetime.timedelta(spended_days)

#                 way_costs = (get_ph_data.get_route_distance_to_wh(start_addr, end_addr) / 100000) * vehicle_consumption * fuel_price

#                 WHTransfer.objects.create(arrival_day=arrival_day, way_costs=way_costs)# wh1_id



    # WHTransferClaim.objects.filter(active=True, )
    # WHProduct.objects.filter(warehouse=True)
    # WHTransferClaim.objects.filter(active=True)
    # whtcs = WHTransferClaim.objects.filter(active=True)
    # [whtc.from_wh.id for whtc in whtcs]
    # from_wh_s = []
    # for whtc in whtcs:
    #     if from_wh_s

def get_quantity_of_whp_to_purchase(whp):
    # 28/7 * 20 == 80 продуктов в среднем за 4 недели продасться \\ ибо мы как раз и будем ждать время по threshold_days по изх покупке и доставке их в аптеку
    return (get_simulation().normal_purch_days / wph.threshold_days) * wph.threshold # (28 / 7) * 

def get_WHTransferClaim_accepttion(whtcs):
    # разпределить whtc по аптекам 

    to_wh_s = list(set(whtc.to_wh for whtc in whtcs)) #просто сами аптеки взять для проверки на то сколько продуков из этой аптеки в ту аптеку пошлется
    from_wh_s = list(set(whtc.from_wh for whtc in whtcs))

    for to_wh in to_wh_s:
        for from_wh in from_wh_s:
            whtc_wh_pair = WHTransferClaim.objects.filter(from_wh=from_wh, to_wh=to_wh)
            quantity = sum(i.quantity for i in whtc_wh_pair)
            if quantity >= get_simulation().number_to_dispatch:
                WHTransferClaim.objects.filter(from_wh=from_wh, to_wh=to_wh).update(accepted=True) #  и отсюда прямиком в трансфер WHTransfer ( при его проверке в конце каждого дня )
                # если мы уже подтвердили что будут продукты отсылатся, то мы их не считаем за свои
                for i in whtc_wh_pair:
                    WHProduct.objects.filter(warehouse=from_wh, product=i.product).update(soon_expire=True)

                    whp = WHProduct.objects.filter(warehouse=from_wh, product=i.product)

                    PurchaseClaim.objects.create(quantity=get_quantity_of_whp_to_purchase(whp), whp=whp)

                WHTransfer.objects.create(from_wh=from_wh, to_wh=to_wh) # WHTransferClaim.objects.filter(from_wh=from_wh, to_wh=to_wh, accepted=True)


# WHTransferClaim claims witch will executed (they accepted)
def set_transfer_products(): # one time in 4 week normally should expire 28 / 7
    """ создаем WHTransferClaim потом WHTransfer и PurchaseClaim а потом еще PurchaseClaim"""
    whps_to_WHTransferClaim = WHProduct.objects.filter(quantity=0) # те что оч важно быро доставить ( а сразу пишем в покупку к вендору  но и в WHTransferClaim для заимствования из других аптек - если там нет лишнего - то ничего не делаем)
    whps_from_WHTransferClaim =  WHProduct.objects.filter(soon_expire=False)

    # для того чтоб дважды не заказывать сун експаир из get_WHTransferClaim_accepttion и отсюдова - делаем запрос на сун_експаир до get_WHTransferClaim_accepttion
    whps_to_PurchaseClaim = WHProduct.objects.filter(soon_expire=True)  # те что не оч важно быро доставить ( а сразу пишем в покупку к вендору)

    # whs_from_WHTC = 
    # products одинаковые но с разных аптек
    # создаем всевозможные клемы # мб до 43 * 1 * 100 или 22 * 22 * 100 =48 400 клеймов максимум следовательно from_wh и to_wh чисто физически не могут повторятся
    whtcs = []

    # from_wh_s = [[] for i in range(len(whps_from_WHTransferClaim))]
    # to_wh_s = []
    for whp1 in whps_from_WHTransferClaim: 
        for wph2 in whps_to_WHTransferClaim:
            dispathed_quantity = (wph1.quantity - wph1.threshold)
            # if избыток более-равно недостатку - отсылаем с запасом , да так, чтоб у того от кого отослали сразу был в запрос уже на закупку у вендора
            if dispathed_quantity >= wph2.expire_quantity: # check_WHTransferClaim_on_asseption приямо сдесь, чтоб зря не создавать клеймы
                # сколько я могу послать из избыточной в недостаточную
                # first WHTransferClaim creation
                whtc = WHTransferClaim.objects.create(from_wh=whp1.warehouse, to_wh=wph2.warehouse, product=wph2.product, quantity=dispathed_quantity) # закупка на колличество которые запросили уже
                whtcs.append(whtc)

    get_WHTransferClaim_accepttion(whtcs)

    # WHTransferClaim.objects.filter(accepted=True, started=False) # - знач просто ждут своих машин которые в пути для других аптек



    # при его исполнении пополняется PurchaseClaim когда  whtcs = WHTransferClaim.objects.filter(accepted) self.started=True в  WHTransfer
    # whtcs = self.WHTransferClaim.filter(accepted=True)
    # for whp in [WHProduct.objects.get(warehouse=whtc.from_wh, product=whtc.product) for whtc in whtcs]:
    #     PurchaseClaim.objects.create(quantity=get_quantity_of_whp_to_purchase(whp), whp=whp)

    # perform_WHTransfer(whs, fuel_price, vehicle_consumption)

    # TODO HERE 
    # check_WHTransferClaim_on_asseption() # получить те клеймы которые пойдут в WHTransfer

    # add reserved PurchaseClaim objects
    for whp in whps_to_PurchaseClaim:
        # 28/7 * 20 == 80 продуктов в среднем за 4 недели продасться \\ ибо мы как раз и будем ждать время по threshold_days по изх покупке и доставке их в аптеку
        PurchaseClaim.objects.create(quantity=get_quantity_of_whp_to_purchase(whp), whp=whp)

    # WHProduct.objects.filter(quantity=0)
    # WHProduct.objects.filter(soon_expire=True)




# как только 1 клейма expire_day - все остальные которые не екзекьютед - посылаются в пурчейз
# def PurchaseClaim_simulation():
# receiver
# instance.tax = TaxRate.objects.get(name='for_Sale')

# if we just call Sale.objects.create() -> all fields are populated and then stored ( and used for DF )
class Sale(models.Model): # every day                                   # for every pharmacy
    """
    quantity_rate_per_day - always the same as settled ( but whproduct.self_rate can change for each product in each pharmacy)
    always учитывается рейт как процент от всего количества товара в аптеке, тоесть чтоб за месяц норм продать все количество продукта надо рейт не менее 3.3 ежедневно (~3.3%*~30 == ~ 100)
    вывод - для выборки choices['sales_quantity_rate_ranges_per_day'] все что более 0.03 - вероятно будет продоватся полностью

    при создании заполняем только:  quantity_rate_per_day   and    warehouse 
    """
    # quantity_rate_per_day = models.DecimalField(max_digits=3,
    #                                 decimal_places=2,
    #                                 validators=[MinValueValidator(D('0')),
    #                                             MaxValueValidator(D('1'))])

    # # substituted by random day_quantity_range
    # quantity_rate_per_day = models.FloatField(default=0.0) # для рандома при покупках за сутки
    min_day_quantity = models.IntegerField(max_length=8)
    max_day_quantity = models.IntegerField(max_length=8)
    warehouse = models.ForeignKey('WareHouse', related_name='sales', on_delete=models.SET_NULL)  # for every pharmacy
    # те которые закончились или скоро закончатся 
    # 1) те что закончились уже - ищем у других аптек пока что  и делаем клейм 
    # 2) те которые скоро истекут - просто в клейм (threshold*4 ( 4 weeks - month))
    # 3) как раз таки threshold_days == (количеству дней для клейма) (минус) ( дни на доставку (3))
    # expire_whp = models.ManyToManyField('WHProduct', related_name='sales', on_delete=models.SET_NULL) # if we somehow gonna delete  wh or whp thats doesnt mean that sale will be deleted
    # whproduct.add(WHProduct1, ...)
    # whproducts = models.ManyToManyField('WHProduct', related_name='sales') # related_name='sales' # some whproducts can be there ( каждый сейл = количеству whproduct-а в соответствии с рейт)
    # quantity = models.IntegerField(max_length=10)
    total_price = models.FloatField(default=0.0) # продаем сразу с учетом ндс так как и купили с ндс, потому при продаже не отнимаем ндс (tax)
    tax = models.ForeignKey(TaxRate, related_name='sales', on_delete=models.CASCADE)
    # total_price = models.DecimalField(max_digits=12, decimal_places=2, default=D('0.00'))
    

@receiver(pre_save, sender=Sale)
def set_sale_quantity(sender, instance, *args, **kwargs):
    # if quantity is settled -> Sale already is performed
    if not instance.total_price and not instance.whproducts:
        whps = WHProduct.objects.filter(warehouse__id=instance.warehouse.id)
        for whp in whps: 
            # instance.whproducts.add(whp)
            # transfer quantity

            # substituted by random day_quantity_range
            # saled_quantity = int(whp.self_rate * instance.quantity_rate_per_day * whp.quantity) # до нижнего порога округлит
            saled_quantity = int(random.choice(range(self.min_day_quantity, self.max_day_quantity)) * whp.self_rate) # example: 5*0.8=int(4.0) or 4*1.2=int(5.0)
            
            DemandForecasting.objects.create(saled_quantity=saled_quantity, wh=whp.warehouse, product=whp.product) # 4500 строк в дф в день
            # whp.last_saled_quantity = saled_quantity
            if (whp.quantity - saled_quantity) >= 0:
                whp.quantity = whp.quantity - saled_quantity
            else:
                # ne hvatilo tovara po zaprosy
                lack = saled_quantity - whp.quantity
                # недостаток за каждый день добавляем в экспаир квонтити
                whp.expire_quantity  += lack
                # all whp in pharmacy is saled
                whp.quantity = 0
            if whp.threshold >= whp.quantity:
                whp.soon_expire = True
            # whp.save()
            whp.save()
            instance.total_price += saled_quantity * whp.product.markup_price # int* decimal norm # but float do not :( -> use D(str())
            
            # after taht should refresh_from_db -> cause there instance.total_price still 0 but in db = saled_quantity * whp.product.markup_price
            instance.refresh_from_db()
        instance.tax = TaxRate.objects.get(name='for_Sale')
        instance.save()
        # отослать это все в активы и пассивы - не поодиночно - потому после создания сейла

        # сделать заявку на покупку недостающих товаров или товаров , которые вот-вот закончатся 
        # порог:  whp.threshold = sum(int(random.choice(range(self.min_day_quantity, self.max_day_quantity)) * whp.self_rate) for i in range(7)) - тоесть rand значение по закупке за неделю
        
            # max_days_on_delivery должны равнятся занчению из (100% на задержки в пути + сам путь который подсчитан в роутс в анитегрейтед таскс)
            # если PC от вендора( Центральная точка по УКР - глянуть в дров граф - центр адрес и использывть его) до нас
            # или же просто между аптеками (ищем аптеки с избытком тоесть те, где продуктов больше порога (тоесть левая_аптека.threshold),
            #  забираем у нее все что более порога, но ее кидаем на закупку товара) и так по всем в которых более и отправляем во все в который менее

            # PurchaseClaim.objects.create(expire_day=whp.threshold-max_days_on_delivery, quantity=, whp=)
        #  
        # instance.price = sum(whp.last_saled_quantity for whp in whps)
            # whp.refresh_from_db()

        # instance.whproduct.last_saled_quantity = 0
        # instance.whproduct = instance.whproduct - instance.quantity
        # instance.whproduct.save()
        # calc total whproduct price

@receiver(post_save, sender=Sale)
def Sale_set_A_P(sender, instance, created, **kwargs):
    if created:
        acc_operations.sale_to_account(value=instance.total_price) # sale_to_cassa




def perform_sale(sim):  # from simulation
    whs = WareHouse.objects.all()
    for wh in whs:
        Sale.objects.create(warehouse=wh, min_day_quantity=sim.day_quantity_range[0], max_day_quantity=sim.day_quantity_range[1])
    # клеймы заполнить
    # PurchaseClaim and WHTClaim created here
    set_transfer_products()
    # проверка на истекающие клеймы для покупок
    check_on_start_purchases()
    # подитожить какие клеймы на обработку 
    # ( тоесть либо пересылку меж аптеками либо на закупку) 
    # если на пересылку не насобиралось ( тоесть менее 300 продуктов с аптеки до аптеки) 
    # то тоже послать все в 
    # стоп
    # вообще все в пурчейзклейм
    # а там де оч мало проверка на трансфер, но от этого мб добавятся еще пурчейзклеймы на те аптеки с которых спыздылы лишнее пересылки
    # claimed_WHT_whs = WareHouse.objects.filter()
    # perform_WHTransfer(whs, fuel_price, vehicle_consumption) # добавить пересылку (если добавилась то в итоге еще и PC добавятся) потому только строго потом делать perform_Purchase
    # perform_Purchase()

    # DemandForecasting.objects.create()
        # Sale.objects.create(warehouse=wh, quantity_rate_per_day=sales_quantity_rate_ranges_per_day)

# # /\/\ TODO perform DF
class DemandForecastingReport(models.Model): # # end month
    # from calendar import monthrange 
    # import datetime 
    #
    # that_month_day = get_simulation().today
    # days_in_month = monthrange(that_month_day.year, that_month_day.month)[1]
    # 
    # DemandForecastingReport.date_to_report = get_simulation().today + datetime.timedelta(days_in_month)
    # DemandForecastingReport.created = that_month_day # по идее автоматически если поле поменяем на DateField() то впишем


    # if DemandForecastingReport.date_to_report = get_simulation().today
    #   DemandForecastingReport.get_report()
    # if DemandForecastingReport.created
    created = MyDateField(auto_now_add=True)
    date_to_report = models.DateField(blank=True)
    reported = models.BooleanField(default=False)
    wh = models.ForeignKey("WareHouse", related_name='purchases', on_delete=models.CASCADE) # setting while creating потому что надо не потерятся какой Purchase заменять, с какой аптекой
    demanded = ArrayField(models.IntegerField(max_length=10), blank=True)

    def get_report(self):
        month_dfs = self.demand_forecastings.all()  # каждого продукта в аптеке ибо в сейлсах - DemandForecasting.objects.create для каждого продукта в аптеке
        forecast_data = [{"wh": daily_df_in_wh.wh.pharmacy_number, "product": daily_df_in_wh.product.name, "saled_quantity": daily_df_in_wh.saled_quantity} for daily_df_in_wh in month_dfs] # for one wh for month
        self.demanded = forecast(forecast_data) # сколько продуктов надо на эту аптеку
        self.reported = True
        self.save()

        that_month_day = get_simulation().today
        days_in_month = monthrange(that_month_day.year, that_month_day.month)[1]
        date_to_next_report = that_month_day + datetime.timedelta(days_in_month)
        DemandForecastingReport.objects.create(wh=wh, date_to_report=date_to_next_report) # created auto

# @receiver(pre_save, sender=DemandForecasting)
# def set_DF_values(sender, instance, *args, **kwargs):
#     if not instance.to_report:
#         DemandForecastingReport.objects.get(wh=instance.wh, reported=False)
#         instance.save()

class DemandForecasting(models.Model): # daily on each whp 
    wh = models.ForeignKey('WareHouse', related_name='demand_forecastings', on_delete=models.CASCADE)
    product = models.ForeignKey('Product', related_name='demand_forecastings', on_delete=models.CASCADE)
    saled_quantity = models.IntegerField(max_length=10) # м ы тут не указываем продажи а запросы только, потому именно saled_quantity записываем из сейлов
    to_report = models.ForeignKey(DemandForecastingReport, related_name='demand_forecastings', on_delete=models.CASCADE)
    # sale_in_whs = models.ManyToManyField(Sale, related_name='demand_forecastings', on_delete=models.SET_NULL) # все сейлсы за день по каждой аптеке

    # # заполнается селом

@receiver(pre_save, sender=DemandForecasting)
def set_DF_values(sender, instance, *args, **kwargs):
    if not instance.to_report:
        DemandForecastingReport.objects.get(wh=instance.wh, reported=False)
        instance.save()


class WareHouse(models.Model):
    address = models.OneToOneField(Address, on_delete=models.CASCADE, related_name='warehouse')
    pharmacy_number = models.IntegerField(max_length=10)

class Product(models.Model):
    """
    markup_rate - процент наценки ( 20 - 30 от себестоимости)
    cost_price - себестоимость
    markup_price  - вычесляется -> cost_price * (1 + markup_rate)
    """
    # cost_price = models.DecimalField(max_digits=10,
    #                                 decimal_places=2)
    # markup_rate = models.DecimalField(max_digits=3,
    #                                 decimal_places=2,
    #                                 validators=[MinValueValidator(D('0')),
    #                                             MaxValueValidator(D('1'))])
    # markup_price = models.DecimalField(max_digits=10,
    #                                 decimal_places=2)
    cost_price = models.FloatField(default=0.0)
    markup_rate = models.FloatField(default=0.0)
    markup_price = models.FloatField(default=0.0)
    
    name = models.TextField()
    dozation = models.CharField(max_length=30)
    # kind = models.CharField(max_length=30) # таблетки, сироп, спрей, субстанция, порошок, напиток, пастилки, 

@receiver(pre_save, sender=Product)
def get_markup_price_Product(sender, instance, *args, **kwargs):
    if instance.markup_price == 0.0:
        instance.markup_price = instance.cost_price * instance.markup_rate

class WHProduct(models.Model):
    """
    Each product in each warehouse (and its quantity)
    """
    quantity = models.IntegerField(max_length=10)
    # last_saled_quantity = models.IntegerField(max_length=10, default=0) # сколько продали за последний раз - для подсчета полной прибыли по всей аптеке # can be blank if any sales before # после создания сейла по этому квонтити - обратно возвращаем =0
    product = models.ForeignKey(Product, related_name='whps', on_delete=models.CASCADE) # для такого то продукта такие  аптеки
    warehouse = models.ForeignKey(WareHouse, related_name='whps', on_delete=models.CASCADE) # для такой то аптеки такие типы продуктов
    # домножаем quantity_rate_per_day в сейлс на этот кеф  -- может увеличить начальный кеф до 1000% (если поле==9.99 -> quantity_rate_per_day*9.99)
    # тоесть, если изначально sales_quantity_rate_ranges_per_day = 5 проц - домножили на 9 -> = 45 проц - значит что почти половину всего колличества этого товара из аптеки выкупят
    # self_rate = models.DecimalField(max_digits=2, decimal_places=1) # == random(0.8, 1.2)  мы выбрали выборку рандома 0.1 - 5.0

    # substituted by random day_quantity_range
    self_rate = models.FloatField(default=0.0)
    threshold = models.IntegerField(max_length=10)
    threshold_days = models.IntegerField(max_length=10)
    expire_quantity = models.IntegerField(max_length=10, default=0) # сколько не хватеат (сколько пользователи запросили, но не получили да сих пор)
    soon_expire = models.BooleanField(default=False)


class Department(models.Model): # only 1 model in erp // cause only 1 dpt on all company
    organisation = models.CharField(max_length=30) # 'Сеть Аптек "Копейка"'
    address = models.CharField(max_length=30) # "Nezalezhnosti Blvd, 12, Brovary, Kyivs'ka oblast, Ukraine, 07400"


class Fuel(models.Model):
    # from site https://index.minfin.com.ua/markets/fuel/detail/
    fuel_type = models.CharField(max_length=30) # A-95   # А 92  # ДТ    # Газ 
    fuel_price = models.FloatField(default=0.0) # 28.73  # 27.00 # 27.80 # 13.20


class Vehicle(models.Model):
    # from site  tax on price https://www.juridicheskij-supermarket.ua/page_car-tax.html
    # from site http://www.navi39.ru/faqarticle/norma-rashoda-topliva/126-bazovye-normy-rashoda-topliva-dlya-gruzovikov-i-gruzovogo-transporta.html
    vehicle_consumption = models.FloatField(default=0.0) # 9.0
    vehicle_name = models.CharField(max_length=30) # Ford Transit FT-190L
    vehicle_price = models.FloatField(default=0.0) # 25000.00
    fuel = models.ForeignKey(Fuel, related_name='vehicles', on_delete=models.CASCADE)
    # every month changed by perform_Veh_repair_Payment()
    veh_repair_price_month = models.FloatField(default=0.0)

    used_now = models.BooleanField(default=False) # Vehicle.objects.filter(used_now=False).exists()
    # full_address will write in this field 
    vehicle_full_address_now = models.TextField() #models.ForeignKey(Address, related_name='vehicles', on_delete=models.CASCADE)

    go_from_addr = models.TextField()
    go_to_addr = models.TextField()
    transfering = models.BooleanField(default=False)