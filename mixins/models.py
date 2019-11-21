# from django.db import models
# from django.contrib.auth.models import User
# from django.db.models.signals import post_save, pre_save
# from django.dispatch import receiver
# from django.urls import reverse

# from markdown_deux import markdown
# from django.utils.safestring import mark_safe
# from django.utils.text import slugify

# from datetime import datetime

# # from . import simulation

# # info from accounts.models
# # будет рекурсивное импртирование, если будем использывать address тут и импортить его в операции предприятия,, ибо там отсюда импортится вендор
# # WareHouse in c_o and Vendor in accounts

# #/\/\ address using in wh and in profiles> so its mixin
# class Address(models.Model):
#     # address
#     # example: address_line = "ulʹvar Oleksandriysʹkyy, 95", city = "Bila Tserkva", Kyivs'ka oblast, country= 'Ukraine', postal_code='09100'
#     address_line = models.CharField(max_length=128) # street // prospect // enter there an address # first 2 elems in list after strip by ',' 
#     city = models.CharField(max_length=64)
#     region = models.CharField(max_length=128)
#     country = models.CharField(max_length=50)
#     postal_code = models.CharField(max_length=7)


#     def full_address(self, separator="\t"):
#         """
#         Return the non-empty components of the address
#         """
#         fields = [self.address_line, self.city, self.region, self.country, self.postal_code]
#         fields = [f.strip() for f in fields if f]
        
#         return separator.join(fields) # or filter(bool, fields)


#     def __str__(self):
#         return self.full_address()



# class Simulation(models.Model):
#     # changed every simul day
#     today = models.DateField(auto_now=False, auto_now_add=False)

# # from string to datetime: time.strptime
# # from datetime to string: time.strftime


# # one time per sim day
# def set_simul_date(month, day, year):
#     # симуляционный обьект посути будет 1 только for each simulation
#     sim = Simulation.objects.all().last()
#     datetime_str = f'{month}/{day}/{year}'
#     datetime_object = datetime.strptime(datetime_str, '%m/%d/%y')
#     sim.today = datetime_object
#     sim.save()

# # simulational date_today:

# # many times per sim day
# def simulation_datetime_date_today():
#     """ only date returned """
#     return (Simulation.objects.all().last()).today



# # we change in C:\Users\maxul\envs\diplom\lib\site-packages\django\db\models\fields\__init__.py 
# # 1250 row from 
# # value = datetime.date.today() to 
# # value = simulation.date.today()

# class MyDateField(models.DateField):
#     # nihuya ne fact
#     def pre_save(self, model_instance, add):
#         if self.auto_now or (self.auto_now_add and add):
#             value = simulation_datetime_date_today()
#             setattr(model_instance, self.attname, value)
#             return value
#         else:
#             return super().pre_save(model_instance, add)