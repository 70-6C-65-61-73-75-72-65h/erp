from django.db import models
from django.contrib.auth.models import User, Group
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.urls import reverse
from django.apps import apps

from markdown_deux import markdown
from django.utils.safestring import mark_safe
from django.utils.text import slugify

from django.core.validators import MinValueValidator, MaxValueValidator
from decimal import Decimal as D

from django.core.exceptions import FieldDoesNotExist
from simulation.models import get_simulation

# from company_operations.models import Department, Vehicle, WareHouse

from mixins.models import Address, MyDateField

# Create your models here.

# Create your models here.
class Profile(models.Model): # fields
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True, null=True)
    # location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    slug = models.SlugField(unique=True) # unigue url must be
    # avatar = models.ImageField(upload_to=f"profile_photos/{user.username}/{filename}",  # TODO create class Avatar(models.Model) and foreignkey to Profile
    #     null=True,
    #     blank=True,
    #     width_field="width_field", 
    #     height_field="height_field")
    # height_field = models.IntegerField(default=0)
    # width_field = models.IntegerField(default=0) 
    # bank_acc = models.OneToOneField("BankAccount", on_delete=models.CASCADE, related_name='profile')


    # how to add bank_acc to client or some_who
    bank_acc = models.CharField(max_length=16, blank=True, null=True)
    # def decor_role_changing(self, func):
    #     def inner(self, *args, **kwargs):
    #         # args - 
    #         self._meta.get_field(args)
    #         func()
    #     return inner

    def group_changing(self, new_name):
        # print('group changing start')
        # print(self.user.groups.all())
        # print('group_changing start')
        self.user.groups.clear()
        # print('group_changing groups clear')
        # print(self.user.groups.all())
        # print('group changing clear')
        # if self.user.groups.filter(name=old_name).exists():
        g = Group.objects.get_or_create(name=new_name)
        # print('after group getting group')
        # print(g)
        group = g[0]
        # print('after group getting group')
        # print(group)
        # print(group)
        # print('group changing create new')
        # group.user_set.add(self.user)
        self.user.groups.add(group)
        # print('after group adding')
        self.user.save()
        # print('after group saving')
        # print('group changing added to user')
        # (self.user.groups._meta.get_field(f'{old_name}_set')).remove(self.user)
        # self.user.save()
        # self.save()
        # self.user.groups.save() ?????
 
    def role_to_vendor(self, organisation, address):
        try:
        #     # assert self.client.all() is not None
            # print('start role_to_vendor')
            if hasattr(self, 'client'):
                # print('hasattr client')
                self.client.delete()
                # print('hasattr client deleted')
                self.group_changing('vendor')
                # print('group changed to vendor')
                Vendor.objects.create(profile=self, organisation=organisation, address=address)
                # print('vendor obj created')
            elif hasattr(self, 'worker'):
                self.worker.delete()
                self.group_changing('vendor')
                Vendor.objects.create(profile=self, organisation=organisation, address=address)
            elif hasattr(self, 'vendor'):
                print('Its already a vendor role')
                return False
        # except Exception:
        #     pass
        # try:
            # assert self.worker is not None
            # self.worker.delete()
            # self.group_changing('vendor')
            # Vendor.objects.create(profile=self, organisation=organisation, address=address)
        # except Exception:
        #     pass
        # try:
            # assert self.vendor is not None
            # print('Its already a vendor role')
            # return False
        except Exception:
            print('some fucking error')
            return None

    def role_to_worker(self, kind, salary, address, id_workon_place):
        try:
            if hasattr(self, 'client'):
                # print('start client deletion')
                self.client.delete()
                # print('end client deletion')
                # print(f"kind:{kind}")
                # print('before group_changing')
                self.group_changing(f'worker_{kind}')
                # print('after group_changing')
                # print('Here must be created object of worker')
                return Worker.objects.create(profile=self, kind=kind, salary=salary, address=address, id_workon_place=id_workon_place)
                # self.save()
            # elif hasattr(self, 'vendor'):
            #     self.vendor.delete()
            #     self.group_changing(f'worker_{kind}')
            #     Worker.objects.create(profile=self, kind=kind, salary=salary, address=address)
            elif hasattr(self, 'worker'):
                print('Its already a worker role')
                return False
        except Exception as ex:
            print('some fucking error')
            print(ex)
            return None

    def change_worker_class(self, kind, salary):
        try:
            if hasattr(self, 'worker'):
                self.worker.kind = kind
                self.worker.salary = salary
                # self.worker.all().last().refresh_from_db()
                self.worker.save()
                self.group_changing(f'worker_{kind}')
                return True
        except Exception:
            print('there is no such worker models')
            return False

    def role_to_client(self):
        try:
            # if hasattr(self, 'vendor'):
            #     self.vendor.delete()
            #     self.group_changing('client')
            #     Client.objects.create(profile=self)
            if hasattr(self, 'worker'):
                self.worker.delete()
                self.group_changing('client')
                Client.objects.create(profile=self)
            elif hasattr(self, 'client'):
                print('Its already a client role')
                return False
        #     assert self.vendor is not None
        #     self.vendor.delete()
        #     self.group_changing('client')
        #     Client.objects.create(profile=self)
        #     return True
        # except Exception:
        #     pass
        # try:
        #     assert self.worker is not None
        #     self.worker.delete()
        #     self.group_changing('client')
        #     Client.objects.create(profile=self)
        #     return True
        # except Exception:
        #     pass
        # try:
        #     assert self.client is not None
        #     print('Its already a client role')
        #     return False
        except Exception:
            print('some fucking error')
            return None

# mb prihuyarit decotator
    # def change_client_to_vendor(self, organisation): # True - successfully created # False - already created
    #     #________________________________________________________
    #     # def to_vendor(self, organisation)
    #     # try:
    #     #     assert self.client is not None
    #     #     self.client.delete()
    #     #     Vendor.objects.create(profile=self, organisation=organisation)
    #     #     return True
    #     # except Exception:
    #     #     pass
    #     # try:
    #     #     assert self.worker is not None
    #     #     self.worker.delete()
    #     #     Vendor.objects.create(profile=self, organisation=organisation)
    #     #     return True
    #     # except Exception:
    #     #     pass
    #     # try:
    #     #     assert self.vendor is not None
    #     #     print('Its already a vendor role')
    #     #     return False
    #     # except Exception:
    #     #     pass
    #     #________________________________________________________
    #     # if dont already set it (as admin) from client to worker or vendor
    #     try:
    #         self._meta.get_field('client')
    #         # or not settled ( possible break idk where)
    #         # /\/\ check is it a problem after relation deleted (if yes client filed stay here in self but with value None)
    #         assert self.client is not None
    #         # do stuff
    #         self.client.delete()
    #         Vendor.objects.create(profile=self, organisation=organisation)
    #         return True
    #     except (FieldDoesNotExist, AssertionError):
    #         print('client relative model already substituted by vendor model or to worker model\n\
    #              if you want substitute worker to vendor - create new acc')
    #         return False
    #     # except AssertionError:
    #     #     print('some weird error in func "change_client_to_vendor" with assertion ')
    
    # def change_client_to_worker(self, kind):
    #     try:
    #         self._meta.get_field('client')
    #         assert self.client is not None
    #         self.client.delete()
    #         Worker.objects.create(profile=self, kind=kind)
    #         return True
    #     except (FieldDoesNotExist, AssertionError):
    #         print('client relative model already substituted by vendor model or to worker model\n\
    #              if you want substitute vendor to worker - create new acc')
    #         return False

    # def change_worker_to_vendor(self, organisation):

    # def change_vendor_to_worker(self, kind):


   
    def __str__(self):
        return f'profile {self.user.username}'
        # Instance of 'OneToOneField' has no 'username' memberpylint(no-member) - pep-пиздеж

    # @property
    # def get_absolute_url(self):
    #     return reverse("accounts:profile", kwargs={"slug": self.slug})
        
    # @property
    # def get_delete_url(self):
    #     return reverse("accounts:delete", kwargs={"slug": self.slug})

    # @property
    # def get_update_url(self):
    #     return reverse("accounts:update", kwargs={"slug": self.slug})

    def get_markdown(self):
        # print('\n\nget_markdown\n\n')
        # print(self.bio)
        content = self.bio
        markdown_text = markdown(content)
        return mark_safe(markdown_text)

    # class Meta:
    #     ordering = ["-id"]


def create_slug(instance, new_slug=None):
    slug = slugify(instance.user.username)
    if new_slug is not None:
        slug = new_slug
    qs = Profile.objects.filter(slug=slug).order_by("-id")
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" %(slug, qs.first().id)
        return create_slug(instance, new_slug=new_slug)
    return slug

# creation profile right after USER creation
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()


# creation slug right before PROFILE creation
@receiver(pre_save, sender=Profile)
def pre_save_post_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)

# надо добавить поля в User на все данные для клиента и тд
# указывать при создании role_name = TextField() if instance.role_name == "client" -> Client.objects.create(profile=instance)
# if instance.role_name == "worker" Client.objects.create(profile=instance) kind=kind, salary=salary, address=address

# опаа проблема, а как редачить профайл то? будет новые клиенты создавать чтоли?)
# creation Client right after Profile creation
@receiver(post_save, sender=Profile)
def update_user_profile(sender, instance, created, **kwargs):
    """Äfter Profile creation we immidiatly create it as Client, but admin can change it to the Vendor or Worker"""
    if created:
        if not hasattr(instance, "client") and not hasattr(instance, "vendor") and not hasattr(instance, "worker"):
            Client.objects.create(profile=instance)
        # try:
        #     # если хоть раз уже создавали клиента ( даже если потом его удалили), то поле останется, только станет нуль 
        #     # instance._meta.get_field('client')
        #     instance.client.all().exists()
        # except FieldDoesNotExist:
        #     Client.objects.create(profile=instance)
    # instance.save()


#/\/\ mb error in onetone field by 2 sides relation

# при оценке персонала: 
# совокупность нематериальных активов, возникающих в результате действия факторов, которые вызывают экономические выгоды # 11 видов рабочих
# goodwill_koef = {'cleaner': 0.2, 'pharmacist': 1.4, 'accounting_manager': 1.95, 'forecast_manager': 1.95, 
#                   'director': 1.95, 'loader': 0.2, 'driver': 1.15, 'storekeeper_manager': 1.7, 'storekeeper': 1.05,
#                   'sys_admin': 1.7, 'supply_chain_manager': 1.95}  ## 'HR': 1.7
# HumanCapacity = Salary(per month)*goodwill_koef

# class Cleaner(models.Model):
    # goodwin_koef = models.DecimalField(max_digits=4, decimal_places=3)


# TODO:#
# #     min_salary = 4173  # (hrn)

# #     tax_auto = 25000 # (hrn)
# #     limit_salaries_auto_cost = 375
# #     num_auto = 20
# #     # list of costs for each auto ( automaticly random of costs between 100k - 1mln) (100k ,110,...990, 1000k)
# #     auto_costs = list(map(lambda: random.randrange(100000, 1000001, 10000), range(num_auto)))
    
# #     num_garage = num_auto
# #     # garage 12 - 20 meters
# #     garage_meters = list(map(lambda: random.randrange(12, 21, 2), range(num_garage)))

# #     num_pharmacies = 138
# #     # pharmacy 25 - 50 meters
# #     pharmacies_meters = list(map(lambda: random.randrange(25, 51, 1), range(num_pharmacies)))

# #     num_department = 1
# #     department_meters = list(map(lambda: random.randrange(300, 361, 10), range(num_department)))

# #     num_warehouse = 3
# #     warehouse_meters = list(map(lambda: random.randrange(400, 600, 10), range(num_warehouse)))




# # # autametive insert values : 
# # min_salary : 4173
# # On_Company_Profit_tax : 18%
# # NDS_tax : 20%
# # Single_tax : 5%
# # On_Property_tax : 1.5% * min_salary * meters
# # On_Garage_tax : 0,01% * min_salary * meters
# # On_Auto_tax : 25000/12 в месяц # Ставка налога в годовом измерении составляет 25 тыс. грн за одну единицу автотранспорта
# # On_Salary_Profit_tax : 18%



# class TaxRate(models.Model): # несолько видов налогов все описаны в таких строках модели
#     name = models.CharField(max_length=50)
#     rate = models.DecimalField(max_digits=6,
#                                decimal_places=5,
#                                validators=[MinValueValidator(D('0')),
#                                            MaxValueValidator(D('1'))])

#     def __str__(self):
#         return f"Tax {self.name}, with {self.rate} rate"


# # import ast

# class CompanyConsts(models.Model):
#     """
#     how to get value:
#     # ast.literal_eval(value)
#     # """
#     name = models.CharField(max_length=50)
#     value = models.TextField(default='') # list or integer ...  -> list to str -> ast.literal_eval

#     def __str__(self):
#         return f'company const - {name}'


# #""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""" in another app called "accounting""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# class Salary(models.Model):
#     value = models.DecimalField(max_digits=7, # more then 100к hrn you cant get
#                                decimal_places=2)
#     tax = models.ForeignKey(TaxRate, on_delete=models.CASCADE, related_name='salaries')


# # class Profit(TaxRate, models.Model):


# # class Purchase(TaxRate, models.Model): # покупки ( у вендора ) # в один чек?
# #     value = models.DecimalField(max_digits=10, # more then 100млн hrn you cant get
# #                                decimal_places=2)
# #     # tax = models.ForeignKey(TaxRate, on_delete=models.CASCADE, related_name='sales')


# # class Sale(TaxRate, models.Model): # продажи ( клиентам ) # в один чек?
# #     value = models.DecimalField(max_digits=10, # more then 100млн hrn you cant get
# #                                decimal_places=2)
# #     tax = models.ForeignKey(TaxRate, on_delete=models.CASCADE, related_name='buys')
# #""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""" in another app called "accounting""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

# class EquipmentService(models.Model):


# # class Vehicle(models.Model):

# # property - недвижимость; 
# # possessions- имущество

# class Property(models.Model): # 4 штуки всего в бд (Car, Warehouse, Pharmacy, Department)
#     """ 
#     Part of Assets
#     #active account # more debit - more actives (maybe and properties)
#     """
#     debit_balance = models.DecimalField(max_digits=10, # more then 100mln hrn you cant get
#                                decimal_places=2)
    
# class CalculateCurrentProperty:
#     # calc HumanCapacity
#     #
#     # in -> Property, -> 
#     def get_balance(self):
#         debit_balance =

#     # prop_type = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='')# models.CharField(max_length=100) # 1) Car, 2) Warehouse rent (or price of wh), 3) Pharmacies, 4) Manager Building with offices (department) 5)
#     # meters = models.IntegerField(max_digits=4)
#     # taxes  = models.IntegerField()
#     # price = models.DecimalField(max_digits=10, decimal_places=2) # price of Car, ... # для подсчета акитвов предприятия ( а именно ценности имущества)
#     # year_service
#     # quantity = 


# class Garage(models.Model):
#     meters = models.ForeignKey(CompanyConsts, on_delete=models.CASCADE, related_name='') # square meters

# class Warehouse(models.Model):
#     meters = models.IntegerField(default=500)

# class Pharmacy(models.Model):
#     meters = models.IntegerField(default=40)

# class Department(models.Model):
#     meters = models.IntegerField(default=360)



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

# # Part of Assets
# class Worker(models.Model):




# class BankAccount(models.Model):
#     number = models.CharField(max_length=16) # 0000 0000 0000 0000
#     bank_name = models.TextField()

#     def __str__(self):
#         return f'{self.bank_name} card: {self.number}'


# админ или хр или бухгалтер
# админ будет вносить

# /\/\ у админа только доступ к созданию моделей Worker и Vendor

class Vendor(models.Model): # user in ProfileMixin - физ представитель производителя, кри представитель производителя, через которого все закупки идут
    organisation = models.TextField()
    profile = models.OneToOneField(Profile, on_delete=models.SET_NULL, related_name='vendor', null=True)
    address = models.OneToOneField(Address, on_delete=models.PROTECT, related_name='vendor')
    # user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='vendor')
    # address = models.OneToOneField(Address, on_delete=models.CASCADE, related_name='vendor')
    # and in Address he put organisation address


# @receiver(pre_save, sender=Vendor)
# def pre_save_vendor_receiver(sender, instance, *args, **kwargs):
#     """
#     adding the group for vendor if it already didnt have it
    
#     for checking permissions in future
#     """
#     if not instance.profile.user.groups.filter(name='vendor').exists():
#         group = Group.objects.get(name='vendor')
#         instance.user.groups.add(group)


class Worker(models.Model):
    # CASCADE - profile when creating - and you can change worker to client any more !!!!!!!!
    profile = models.OneToOneField(Profile, on_delete=models.SET_NULL, related_name='worker', null=True) # 
    address = models.OneToOneField(Address, on_delete=models.CASCADE, related_name='worker')
    kind = models.CharField(max_length=100) # setting in form with casees (HR, Pharmacist, Cleaner ...)
    salary = models.FloatField(default=0.0)# как таковой пересылки на счет нет, подсчитывается пока в селерипеймент все скопом кучей - ибо толку то - все равно мы послать на счет не сможем
    birth_date = models.DateField(null=True, blank=True)
    # salary .... birth_date (mb from profile) and so on
    prob_of_worker_fired = models.FloatField(default=0.0)
    # work_on_wh = models.ForeignKey("company_operations.WareHouse", on_delete=models.SET_NULL, related_name='workers', null=True) # if not only by ids gonna be deleteed / but assesment тоже только по ид а не по аптекам
    # work_on_vehicle = models.ForeignKey("company_operations.Vehicle", on_delete=models.SET_NULL, related_name='workers', null=True) 
    # work_on_dpt = models.ForeignKey("company_operations.Department", on_delete=models.SET_NULL, related_name='workers', null=True)
    work_on_wh = models.BooleanField(default=False)
    work_on_vehicle = models.BooleanField(default=False)
    work_on_dpt = models.BooleanField(default=False)
    id_workon_place = models.IntegerField()
    fired = models.BooleanField(default=False)

@receiver(pre_save, sender=Worker)
def pre_save_Worker(sender, instance, *args, **kwargs):
    if instance.prob_of_worker_fired == 0.0 or not instance.prob_of_worker_fired:
        sim = get_simulation()
        if instance.kind == 'HR':
            instance.prob_of_worker_fired = sim.prob_of_worker_fired_hr
            instance.work_on_dpt = True#apps.get_model('company_operations.Department').objects.get(id=instance.id_workon_place)
        elif instance.kind == 'accounting_manager':
            instance.prob_of_worker_fired = sim.prob_of_worker_fired_am
            instance.work_on_dpt = True#apps.get_model('company_operations.Department').objects.get(id=instance.id_workon_place)
        elif instance.kind == 'pharmacist':
            instance.prob_of_worker_fired = sim.prob_of_worker_fired_ph
            instance.work_on_wh = True#apps.get_model('company_operations.WareHouse').objects.get(id=instance.id_workon_place)
        elif instance.kind == 'director':
            instance.prob_of_worker_fired = sim.prob_of_worker_fired_dir
            instance.work_on_dpt = True#apps.get_model('company_operations.Department').objects.get(id=instance.id_workon_place)
        elif instance.kind == 'cleaner':
            instance.prob_of_worker_fired = sim.prob_of_worker_fired_cl
            instance.work_on_wh = True#apps.get_model('company_operations.WareHouse').objects.get(id=instance.id_workon_place)
        elif instance.kind == 'loader':
            instance.prob_of_worker_fired = sim.prob_of_worker_fired_ld
            instance.work_on_vehicle = True#apps.get_model('company_operations.Vehicle').objects.get(id=instance.id_workon_place)
        elif instance.kind == 'driver':
            instance.prob_of_worker_fired = sim.prob_of_worker_fired_dr
            instance.work_on_vehicle = True#apps.get_model('company_operations.Vehicle').objects.get(id=instance.id_workon_place)
        elif instance.kind == 'sys_admin':
            instance.prob_of_worker_fired = sim.prob_of_worker_fired_sa
            instance.work_on_dpt = True#apps.get_model('company_operations.Department').objects.get(id=instance.id_workon_place)


class Client(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.SET_NULL, related_name='client', null=True)
    # wh = models.ForeignKey("company_operations.WareHouse", on_delete=models.SET_NULL, related_name='clients', null=True)

    def make_assessment(self, assess, worker, pharmacy):
        # не отталкиваемся от сейлов а просто ежедневно проверка на оценку от пользователя  - биноминальное распр по к-ву клиентов которые сегодня сделают оценку в 
        # assess = 
        sim = get_simulation()
        apps.get_model('assessments.Assessment').objects.create(assess=assess, worker=worker, pharmacy=pharmacy, client=self, created=sim.today)
    # address = models.OneToOneField(Address, on_delete=models.CASCADE, related_name='client')

# class Director(Profile, Address): # like admin in rights
#     pass
#     # group = Group.objects.get(name='groupname') 
#     # group = Group.objects.all() # all groups
    
#     # def add_user_group(self): # for checking permissions in future # return None
#     #     map(lambda group: user.groups.add(group), Group.objects.all()) # [user.groups.add(group) for group in groups]

# class Pharmacist(Profile, Address)

# #Product # Vendor

# # class HRSpecialist(models.Model): # functions // methods
# #     # def checkAssessment(self):


# # class ProfileHRSpecialist(Profile, HRSpecialist):


# # class ProfileClient()
    

# pep-пиздежа: 4 