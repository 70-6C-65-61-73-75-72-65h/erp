from django import forms
from .models import Simulation

class SimulationForm(forms.ModelForm):

    class Meta:
        model = Simulation
        fields = [
            # after that - CompanyConsts will be populated

            # to CommunalServisePayment
            "minimal_zp", # float 4173
            "pharmacys_sizes", # float - every is identical to easy calc 40
            "department_size", # float - every is identical to easy calc 300
            "tax_property_size_limit", # float 60.0
            "pharmacys_spendingds", # Array(int, int) - to easy performed random (300-500)
            "department_spendingds", # Array(int, int) - to easy performed random (3000-5000)

            # to Veh_repair_Payment
            "veh_repair_price_month", # Array(int, int) - to easy performed random [3000,6000]
            "vehicles_num", # int ph_num / 5   15% - задержка при доставке
            "vehicle_price", # float
            "fuel_price", # float
            "fuel_type", # str
            "vehicle_consumption", # float

            # Purchase
            "delivery_added_time_koef", # float == 1.15 (must be >=  1)
            # сколько на 1 аптеку машин для доставки  44 апт - 2, 4, 11, 22, 44 выбрать
            # ****to be calculated in pre_save model ******** "num_of_phs_on_1_vehicle" ""int"" # = int(WaheHouse.objects.all().count() / vehicles_num)  # уеличение времени на реализацию доставки  столько раз сколько аптек 
            # default in model "warehouse_num"  -  int =  44

            # for Department
            # "dpt_address", # str "Nezalezhnosti Blvd, 12, Brovary, Kyivs'ka oblast, Ukraine, 07400"
            # "dpt_organisation", # str "Сеть Аптек 'Копейка'"
            # taxes leave auto not changable

        ]

        VEHICALS_NUM = (
                ('', 'Select the vehicles_num to calc amount pharmacies on 1 vehicle'),
                ('1', '1'), #First one is the value of select option and second is the displayed value in option
                ('2', '2'),
                ('4', '4'),
                ('11', '11'), # this to choose !!!
                ('22', '22'),
                ('44', '44'),
                )
        widgets = {
            'vehicles_num': forms.Select(choices=VEHICALS_NUM, attrs={'class': 'form-control'}),
        }