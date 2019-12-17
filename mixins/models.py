from django.db import models
import simulation.models as sim
import datetime
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

# form for Address
#/\/\ address using in wh and in profiles> so its mixin
class Address(models.Model):
    # address
    # example: address_line = "ulʹvar Oleksandriysʹkyy, 95", city = "Bila Tserkva", Kyivs'ka oblast, country= 'Ukraine', postal_code='09100'
    address_line = models.TextField() # street // prospect // enter there an address # first 2 elems in list after strip by ',' 
    city = models.CharField(max_length=100)
    region = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=100)
    full_address = models.TextField()

    # def full_address(self, separator=", "):
    #     """
    #     Return the non-empty components of the address
    #     """
    #     fields = [self.address_line, self.city, self.region, self.country, self.postal_code]
    #     fields = [f.strip() for f in fields if f]
        
    #     return separator.join(fields) # or filter(bool, fields)


    def __str__(self):
        return self.city


class MyDateField(models.DateField):
    # nihuya ne fact
    def pre_save(self, model_instance, add):
        if self.auto_now or (self.auto_now_add and add):
            if sim.get_simulation() is not None:
                value = sim.get_simulation().today
            else:
                value = datetime.date.today()
            setattr(model_instance, self.attname, value)
            return value
        else:
            return super().pre_save(model_instance, add)


# class CompanyConsts(models.Model):
#     name = models.CharField(max_length=60)
#     value = models.CharField(max_length=60) # CompanyConsts.value = str(value) - >  value = ast.literal_eval(CompanyConsts.value) # or float or integer or str can be