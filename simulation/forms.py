from django import forms
from .models import Simulation

class SimulationForm(forms.ModelForm):

    class Meta:
        model = Simulation
        fields = [
            # # after that - CompanyConsts will be populated

            # # to CommunalServisePayment
            # "minimal_zp", # float 4173
            # "pharmacys_sizes", # float - every is identical to easy calc 40
            # "department_size", # float - every is identical to easy calc 300
            # "tax_property_size_limit", # float 60.0
            # "pharmacys_spendingds", # Array(int, int) - to easy performed random (300-500)
            # "department_spendingds", # Array(int, int) - to easy performed random (3000-5000)

            # # to Veh_repair_Payment
            # "veh_repair_price_month", # Array(int, int) - to easy performed random [3000,6000]
            # "vehicles_num", # int ph_num / 5   15% - задержка при доставке
            # "vehicle_price", # float
            # "fuel_price", # float
            # "fuel_type", # str
            # "vehicle_consumption", # float

            # # Purchase
            # "delivery_added_time_koef", # float == 1.15 (must be >=  1)
            # # сколько на 1 аптеку машин для доставки  44 апт - 2, 4, 11, 22, 44 выбрать
            # # ****to be calculated in pre_save model ******** "num_of_phs_on_1_vehicle" ""int"" # = int(WaheHouse.objects.all().count() / vehicles_num)  # уеличение времени на реализацию доставки  столько раз сколько аптек 
            # # default in model "warehouse_num"  -  int =  44

            # # for Department
            # # "dpt_address", # str "Nezalezhnosti Blvd, 12, Brovary, Kyivs'ka oblast, Ukraine, 07400"
            # # "dpt_organisation", # str "Сеть Аптек 'Копейка'"
            # # taxes leave auto not changable



            # все изменяемо кроме warehouse_num и тех что считаются в ресивере




            # to CommunalServisePayment
            "minimal_zp",#models.IntegerField()
            "pharmacys_sizes",#models.FloatField()
            "department_size",#models.FloatField()
            "tax_property_size_limit",#models.FloatField()
            "pharmacys_spendingds",#models.ArrayField(models.IntegerField(), size=2)
            "department_spendingds",#models.ArrayField(models.IntegerField(), size=2)

            # to Veh_repair_Payment
            "veh_repair_price_month",#models.ArrayField(models.IntegerField(), size=2)
            # "vehicles_num",#models.IntegerField() # 4  - no !!!    but  11
            "vehicles_purchase_num",
            "vehicles_whtransfer_num",
            # vehicles and fuel_price and fuel_type are static
            "vehicle_name",#models.CharField(max_length=60, default='Ford Transit FT-190L')
            "vehicle_price",#models.FloatField() # 25000.0
            "fuel_price",#models.FloatField() # 28.73
            "fuel_type",#models.CharField(max_length=60)
            "vehicle_consumption",#models.FloatField() # 9.0
            
            # Purchase and WHTransfer for Purchase
            "delivery_added_time_koef",#models.FloatField() # 1.15 
            # "num_of_phs_on_1_vehicle",#models.IntegerField() # 44/4 == 11   - no !!! but 44/11",#4 num_of_phs_on_1_vehicle
            # "warehouse_num",#models.IntegerField(default=44)

            # for WHTransfer between phs
            "number_to_dispatch",#models.IntegerField(default=300)
            # for creation PurchaseClaim
            "normal_purch_days",#models.IntegerField(default=28)
            # for Purchase
            "threshold_days",#models.IntegerField(default=7) # за сколько дней до предположительного исчерпания продуктов надо делать заявку на закупку

            # for products
            "number_of_products_names",#models.IntegerField() # 100
            "product_markup_rate",#models.ArrayField(models.FloatField(), size=2) # 0.25, 0.3
            "product_cost_price",#models.ArrayField(models.FloatField(), size=2)

            #for whproducts
            "whp_self_rate",#models.ArrayField(models.FloatField(), size=2) # 0.7, 1.5
            "whp_quantity",#models.ArrayField(models.IntegerField(), size=2) # 100, 200

            # for sale                                      for 1 whp in day
            "day_quantity_range",#models.ArrayField(models.IntegerField(), size=2) # 2, 5
            
            # SalaryPayment in accounts.worker creation in _up   == 8 types really worx
            "salary_pharmacist",#models.FloatField(default=7000.0) # salary_pharmacist_num",# warehouse_num*3  #models.ArrayField()
            "pharmacist_per_wh",#models.IntegerField(default=3) # pro zapas 1 (2 odnovremenno)
            # "pharmacist_num",#models.IntegerField()

            "salary_HR",#models.FloatField(default=11000.0)
            "HR_num",#models.IntegerField(default=6) # мониторят оценки в ассесментс модели и могут - уволить \ нанять  pharmacist - но изменения все равно делает админ или нет? могут понизить зп?

            # 1 для проверки ответов системы, так как все операции производятся ерп - системой (1 про запас) - посменно
            "salary_accounting_manager",#models.FloatField(default=8000.0)
            "accounting_manager_num",#models.IntegerField(default=2)
            # accounting_managers_num_per_company",#models.IntegerField(default=1)

            # 1
            "salary_director",#models.FloatField(default=15000.0)

            "salary_cleaner",#models.FloatField(default=5000.0)
            "cleaner_per_wh",#models.IntegerField(default=2) # pro zapas 1
            # "cleaner_num",#models.IntegerField()

            "salary_loader",#models.FloatField(default=7000.0)
            "loader_per_vehicle",#models.IntegerField(default=2) # pro zapas 1
            # "loader_num",#models.IntegerField()

            "salary_driver",#models.FloatField(default=10000.0)
            "driver_per_vehicle",#models.IntegerField(default=2) # pro zapas 1
            # "driver_num",#models.IntegerField()

            "salary_sys_admin",#models.FloatField(default=10000.0)
            "sys_admin_num",#models.IntegerField(default=2)
            
            #initial_num_of_clients_that_make_assesments_and_buys
            "num_of_clients",#models.IntegerField(default=88) 

            # for convinience in opening accounts
            "that_user_password",#models.CharField(default="that_user_111", max_length=30)


        ]

        # VEHICALS_NUM = (
        #         ('', 'Select the vehicles_num to calc amount pharmacies on 1 vehicle'),
        #         ('1', '1'), #First one is the value of select option and second is the displayed value in option
        #         ('2', '2'),
        #         ('4', '4'),
        #         ('11', '11'), # this to choose !!!
        #         ('22', '22'),
        #         ('44', '44'),
        #         )
        # widgets = {
        #     'vehicles_num': forms.Select(choices=VEHICALS_NUM, attrs={'class': 'form-control'}),
        # }
        VEHICALS_NUM = (
                ('', 'Select the vehicles_purchase_num to perform purchase transfering'),
                ('1', '1'), #First one is the value of select option and second is the displayed value in option
                ('2', '2'),
                ('4', '4'),
                ('11', '11'), # this to choose !!!
                ('22', '22'),
                ('44', '44'),
                )
        widgets = {
            'vehicles_purchase_num': forms.Select(choices=VEHICALS_NUM, attrs={'class': 'form-control'}),
        }
        VEHICALS_NUM = (
                ('', 'Select the vehicles_whtransfer_num to perform whtransfer transfering to calc amount pharmacies on 1 vehicle'),
                ('1', '1'), #First one is the value of select option and second is the displayed value in option
                ('2', '2'),
                ('4', '4'),
                ('11', '11'), # this to choose !!!
                ('22', '22'),
                ('44', '44'),
                )
        widgets = {
            'vehicles_whtransfer_num': forms.Select(choices=VEHICALS_NUM, attrs={'class': 'form-control'}),
        }