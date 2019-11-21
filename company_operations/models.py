from django.db import models

from decimal import Decimal as D
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from general_accounting.models import Assets, Passives
from accounts.models import Vendor
from simulation.models import Address, MyDateField
# Create your models here.
import random

# before creating all of that should write (set)
# 1) a quantity of products (on each WareHouse) in WHProduct
# 2) other vals from accounts (written in comments)
# 3) random ranges to sales per day (which amount based on quantity of each product in each wh) -> WHProduct.quantity = 100 -> Sale.that_whproduct = random.
# 4) markup_rate for products (20-30)
# 5) changing all of datetimes fileds that get datefield = auto_now_add and auto_now to editable=true ( and in reciever before creation get simulaton time)

# а когда мне решать когда закупка?
class Purchase(models.Model):
    """
    Our purchases from vendor 
    (where vendor is a person that dealed with us) 
    so we import its model from accounts.models
    """
    vendor = models.ForeignKey(Vendor, related_name='purchases', on_delete=models.CASCADE)
    # there we store products and their quantity to buy # if first and no DemandForecasting rows in table -> use standart baesd on 
    # demanded =

class PurchaseClaim(models.Model):
    # /\/\ automate increasing days to 1)decrease days_to_expire and to 2)change all DateField(editable=True) faster than day will came
    # days_to_expire = models.IntegerField(max_length=1)
    expire_day = models.MyDateField() # auto_now_add = created simulation day  # auto_now = updated simulation day # to add value and edit it every simulation day
    quantity - models.IntegerField(max_length=5)
    whp = models.ForeignKey('WHProduct', related_name='purchase_claims', on_delete=models.CASCADE)
    claim_executed = models.BooleanField(default=False) # already_ordered and not gonna searched in future to purchase


def PurchaseClaim_simulation():

# if we just call Sale.objects.create() -> all fields are populated and then stored ( and used for DF )
class Sale(models.Model): # for every pharmacy
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
    expire_whp = models.ManyToManyField('WHProduct', related_name='sales', on_delete=models.SET_NULL) # if we somehow gonna delete  wh or whp thats doesnt mean that sale will be deleted
    # whproduct.add(WHProduct1, ...)
    # whproducts = models.ManyToManyField('WHProduct', related_name='sales') # related_name='sales' # some whproducts can be there ( каждый сейл = количеству whproduct-а в соответствии с рейт)
    # quantity = models.IntegerField(max_length=10)
    total_price = models.FloatField(default=0.0)
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

            # whp.last_saled_quantity = saled_quantity
            if (whp.quantity - saled_quantity) >= 0:
                whp.quantity = whp.quantity - saled_quantity
            else:
                # ne hvatilo tovara po zaprosy
                lack = saled_quantity - whp.quantity
                # all whp in pharmacy is saled
                whp.quantity = 0
            whp.save()
            instance.total_price += saled_quantity * whp.product.markup_price # int* decimal norm # but float do not :( -> use D(str())
            
            # after taht should refresh_from_db -> cause there instance.total_price still 0 but in db = saled_quantity * whp.product.markup_price
            instance.refresh_from_db() 
        # instance.price = sum(whp.last_saled_quantity for whp in whps)
            # whp.refresh_from_db()

        # instance.whproduct.last_saled_quantity = 0
        # instance.whproduct = instance.whproduct - instance.quantity
        # instance.whproduct.save()
        # calc total whproduct price

def perform_sale(day_quantity_range):
    for wh in WareHouse.objects.all():
        Sale.objects.create(warehouse=wh, min_day_quantity=day_quantity_range[0], max_day_quantity=day_quantity_range[1])
        # Sale.objects.create(warehouse=wh, quantity_rate_per_day=sales_quantity_rate_ranges_per_day)

# /\/\ TODO perform DF
# class DemandForecastingReport(models.Model):


# class DemandForecasting(models.Model):


@receiver(post_save, sender=Sale)
def add_DF_sale_values(sender, instance, created, **kwargs):
    if created:
        DemandForecasting.objects.create(user=instance)
    instance.profile.save()


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