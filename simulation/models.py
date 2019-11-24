# # we change in C:\Users\maxul\envs\diplom\lib\site-packages\django\db\models\fields\__init__.py 
# # 1250 row from 
# # value = datetime.date.today() to 
# # value = simulation.date.today()



from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

# Create your models here.
class Simulation(models.Model):
    # changed every simul day
    created_date = models.DateField(auto_now_add=True)
    today = models.DateField(auto_now=False, auto_now_add=False)
    status = models.BooleanField(default=False)

    today_time = models.DateTimeField(auto_now=False, auto_now_add=False) # hours = minimum
    


    auto_populated = models.BooleanField(default=False)
    # daemon_active = models.BooleanField(default=False)
    # info = models.TextField()

    # to CommunalServisePayment
    minimal_zp = models.IntegerField()
    pharmacys_sizes = models.FloatField()
    department_size = models.FloatField()
    tax_property_size_limit = models.FloatField()
    pharmacys_spendingds = models.ArrayField(models.IntegerField(), size=2)
    department_spendingds = models.ArrayField(models.IntegerField(), size=2)

    # to Veh_repair_Payment
    veh_repair_price_month = models.ArrayField(models.IntegerField(), size=2)
    vehicles_num = models.IntegerField() # 4  - no !!!    but  11
    # vehicles and fuel_price and fuel_type are static
    vehicle_name = models.CharField(max_length=60, default='Ford Transit FT-190L')
    vehicle_price = models.FloatField() # 25000.0
    fuel_price = models.FloatField() # 28.73
    fuel_type = models.CharField(max_length=60)
    vehicle_consumption = models.FloatField() # 9.0
    
    # Purchase and WHTransfer for Purchase
    delivery_added_time_koef = models.FloatField() # 1.15 
    num_of_phs_on_1_vehicle = models.IntegerField() # 44/4 == 11   - no !!! but 44/11 = 4 num_of_phs_on_1_vehicle
    warehouse_num = models.IntegerField(default=44)

    # for WHTransfer between phs
    number_to_dispatch = models.IntegerField(default=300)
    # for creation PurchaseClaim
    normal_purch_days = models.IntegerField(default=28)
    # for Purchase
    threshold_days = models.IntegerField(default=7) # за сколько дней до предположительного исчерпания продуктов надо делать заявку на закупку

    # for products
    number_of_products_names = models.IntegerField() # 100
    product_markup_rate = models.ArrayField(models.FloatField(), size=2) # 0.25, 0.3
    product_cost_price = models.ArrayField(models.FloatField(), size=2)

    #for whproducts
    whp_self_rate = models.ArrayField(models.FloatField(), size=2) # 0.7, 1.5
    whp_quantity = models.ArrayField(models.IntegerField(), size=2) # 100, 200

    # for sale                                      for 1 whp in day
    day_quantity_range = models.ArrayField(models.IntegerField(), size=2) # 2, 5
    
    # SalaryPayment in accounts.worker creation in _up   == 8 types really worx
    salary_pharmacist = models.FloatField(default=7000.0) # salary_pharmacist_num =  warehouse_num*3  #models.ArrayField()
    pharmacist_per_wh = models.IntegerField(default=3) # pro zapas 1 (2 odnovremenno)
    pharmacist_num = models.IntegerField()

    salary_HR = models.FloatField(default=11000.0)
    HR_num = models.IntegerField(default=6) # мониторят оценки в ассесментс модели и могут - уволить \ нанять  pharmacist - но изменения все равно делает админ или нет? могут понизить зп?

    # 1 для проверки ответов системы, так как все операции производятся ерп - системой (1 про запас) - посменно
    salary_accounting_manager = models.FloatField(default=8000.0)
    accounting_manager_num = models.IntegerField(default=2)
    # accounting_managers_num_per_company = models.IntegerField(default=1)

    # 1
    salary_director = models.FloatField(default=15000.0)

    salary_cleaner = models.FloatField(default=5000.0)
    cleaner_per_wh = models.IntegerField(default=2) # pro zapas 1
    cleaner_num = models.IntegerField()

    salary_loader = models.FloatField(default=7000.0)
    loader_per_vehicle = models.IntegerField(default=2) # pro zapas 1
    loader_num = models.IntegerField()

    salary_driver = models.FloatField(default=10000.0)
    driver_per_vehicle = models.IntegerField(default=2) # pro zapas 1
    driver_num = models.IntegerField()

    salary_sys_admin = models.FloatField(default=10000.0)
    sys_admin_num = models.IntegerField(default=2)
    
    #initial_num_of_clients_that_make_assesments_and_buys
    num_of_clients = models.IntegerField(default=88) 

    # for convinience in opening accounts
    that_user_password = models.CharField(default="that_user_111", max_length=30)


    def get_simulation_day(self):
        """Сколько дней прошло с начала симуляции"""
        return (self.today - self.created_date).days

@receiver(pre_save, sender=Simulation)
def Simulation_set_vals(sender, instance, *args, **kwargs):
    if instance.auto_populated:

    if not instance.num_of_phs_on_1_vehicle:
        instance.num_of_phs_on_1_vehicle = int(instance.warehouse_num / instance.vehicles_num) # 11

        instance.pharmacist_num = instance.warehouse_num * instance.pharmacist_per_wh
        instance.cleaner_num = instance.warehouse_num * instance.cleaner_per_wh
        instance.loader_num = instance.vehicles_num * instance.loader_per_vehicle
        instance.driver_num = instance.vehicles_num * instance.driver_per_vehicle

        instance.save()

def get_simulation():
    return Simulation.objects.all().last()

