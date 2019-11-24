from django.db import models
from django.core.exceptions import FieldDoesNotExist

from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

import datetime # datetime.date.today() 

from ast import literal_eval
# from django.utils import timezone
from mixins.models import MyDateField
from simulation.models import get_simulation
# Create your models here.
# class HumanCapacity(models.Model):

# class AccountingBalance(models.Model):

# class Evaluation(models.Model):

#http://www.buhoblik.org.ua/uchet/organizacziya-buxgalterskogo-ucheta/258-plan-schetov-buxgalterskogo-ucheta-ukrainy.html  - не от сюда




# отсюда пиздим все счета https://dtkt.com.ua/documents/dovidnyk/plan_rah/plan-r.html

from django.db.models.signals import post_save, pre_save




class TaxRate(models.Model):
    name = models.CharField(max_length=30)
    rate = models.FloatField(default=0.2)



    
# можно заполнить ( будет 300 гдето)
class OperativeAccounts(models.Model): #  в процессе не будет менятся колличество счетов
    """

    constant values:

    'name' - full name of account operation, 

    'classification' - first digit of number, 

    'subclass'- first and second digits of number, 

    'number' - identifier of unique operative account.
    
    Above values will be recorded in _up.py file that populate db and permanent.



    templorary values:

    'start_saldo_credit' - initial value of saldo by credit for Operative Account 
    (until first TrialBalance recording equals zero),

    'start_saldo_debit'- initial value of saldo by debit for Operative Account 
    (until first TrialBalance recording equals zero),

    Above values stores here until they will be recorded to TrialBalance model (report)
    and then updated to relevant values.

    """
    name = models.CharField(max_length=100)
    classification = models.CharField(max_length=100)
    subclass = models.CharField(max_length=100)
    number = models.CharField(max_length=3) # num to str to access to '0 class'

    start_saldo_credit = models.FloatField(default=0.0) # TODO Decimal  \\\\\ показ в пассиве
    # turnover_credit = models.IntegerField(default=0, max_length=10) 
    # end_saldo_credit = models.IntegerField(default=0, max_length=10) 

    start_saldo_debit = models.FloatField(default=0.0)  # \\\\\ показ в активе
    # turnover_debit = models.IntegerField(default=0, max_length=10)
    # end_saldo_debit = models.IntegerField(default=0, max_length=10) # To here



# TODO queryset поменять везде до минимума запросов в бд

class TrialBalance(models.Model): # каждая новая строка - новый отчет
    """ 
    Model of reports that shows saldos and turnover by credit and debit 

    'Оборотно-сальдовая ведомость == Trial Balance'


    'start_saldo_credit' - initial value of saldo by credit for Operative Account 
    (until first TrialBalance recording equals zero), 

    'turnover_credit' - equals the sum of all credit values of all assets and 
    passives that used that account, 

    'end_saldo_credit' - sum of 'start_saldo_credit' and diffrence of credits by formula,

    'start_saldo_debit'- initial value of saldo by debit for Operative Account 
    (until first TrialBalance recording equals zero),

    'turnover_debit' - equals the sum of all debit values of all assets and
    passives that used that account,

    'end_saldo_debit' - sum of 'start_saldo_credit' and diffrence of debits by formula,

    """

    start_saldo_credit = models.FloatField(default=0.0) # Decimal
    turnover_credit = models.FloatField(default=0.0) # Decimal
    end_saldo_credit = models.FloatField(default=0.0) # Decimal

    start_saldo_debit = models.FloatField(default=0.0) # Decimal
    turnover_debit = models.FloatField(default=0.0) # Decimal
    end_saldo_debit = models.FloatField(default=0.0) # Decimal

    date_created = MyDateField(auto_now_add=True)
    date_report = MyDateField(editable=True, blank=True)# from there we can get the ""period""
    period = models.IntegerField(default=0, max_length=10)

    dicts_of_accs = models.TextField(blank=True) # TODO change on json or array of dicts (its nevermind)

    # class Meta:
    #     ordeding = ['-date_report']

    def get_dicts_of_accs(self):
        return ast.literal_eval(self.dicts_of_accs)

    def get_used_accs_with_values(self):
        """ assets and passives по 1 шт с каждой стороны ( либо по дебету либо по кредиту ) """

        assets = self.assets.all() # так как мы берем собственные привязанные активы к этому отчету, то и их же мы ищем в использываных акках (шоб не захватить старые активы которые уже есть в других отчетах)
        passives = self.passives.all()
        assets_ids = [ass.id for ass in assets]
        passives_ids = [pas.id for pas in passives]
        used_accs_nums = [[ass.number in ass in assets], [pas.number in pas in passives]]
        used_accs_nums = sum(used_accs_nums, [])
        dicts_of_accs = []
        totals = {'accs_credits_total': None, 'accs_debits_total': None, 'turnover_credit': None, 'turnover_debit': None}
        used_accs = OperativeAccounts.objects.filter(number__in=used_accs_nums)

        for used_acc in used_accs:
            # if ass or passives relevant for that TB -> calc them
            used_pass = used_acc.passives.filter(id__in=passives_ids)
            used_ass = used_acc.assets.filter(id__in=assets_ids)
            
            acc_credits_total = sum([pas.credit_value for pas in used_pass]) - sum([ass.credit_value for ass in used_ass]) 
            acc_debits_total = sum([ass.debit_value for ass in used_ass]) - sum([pas.debit_value for pas in used_pass])

            acc_turnover_credit = sum([pas.credit_value for pas in used_pass]) + sum([ass.credit_value for ass in used_ass])
            acc_turnover_debit = sum([ass.debit_value for ass in used_ass]) + sum([pas.debit_value for pas in used_pass])
            
            end_saldo_credit = acc_credits_total + used_acc.start_saldo_credit
            end_saldo_debit = acc_debits_total + used_acc.start_saldo_debit


            # for each acc
            dicts_of_accs.append({'acc_number': used_acc.number, 
                'start_saldo_credit': used_acc.start_saldo_credit, 'start_saldo_debit': used_acc.start_saldo_debit, 
                'turnover_credit': acc_turnover_credit, 'turnover_debit': acc_turnover_debit, # for totals too
                'acc_credits_total': acc_credits_total, 'acc_debits_total': acc_debits_total, # for totals too
                'end_saldo_credit': end_saldo_credit, 'end_saldo_debit': end_saldo_debit})

            # update start saldos in op_acc
            used_acc.start_saldo_credit = end_saldo_credit
            used_acc.start_saldo_debit = end_saldo_debit
            used_acc.save()
            # used_acc.refresh_from_db()

        dict_get_total = lambda key: sum(dict_of_acc[key] for dict_of_acc in dicts_of_accs)

        totals['all_credits_total'] = dict_get_total('acc_credits_total') 
        totals['all_debits_total'] = dict_get_total('acc_debits_total') 
        totals['all_turnover_credit'] = dict_get_total('turnover_credit') 
        totals['all_turnover_debit'] = dict_get_total('turnover_debit') 

        return dicts_of_accs, totals

    
        # [ass.credit_value for ass in assets]
        # all_oa = OperativeAccounts.objects.all()#filter(assets=)
        # used_accs_all_asses = [oa for oa in all_oa if len(oa.assets.all()) != 0 or len(oa.passives.all()) != 0] # есть хоть 1 актив для єтого акка привязаній ( по-сути производился)
        # used_accs_all_passes
        # used_accs_for_period = [legit_accs for legit_accs in used_accs_all if legit_accs.operative_day ] # legit_accs - accs to calc values in this instance
        # a_set = self.assets.filter(op_acc__in=used_accs) # ass.op_acc() for ass in a_set
        # p_set = self.passives.all()
        # credit_set = 

    def get_report(self):
        """"after call creating report of TrialBalance
        can call only after creating of TrialBalance instance
        """"
        # перед подсчетом всех компонентов необходимо создать новый баланс, чтоб туда могли записыватся те активы и пассивы которые создаются пока производятся подсчеты для этого отчета
        TrialBalance.objects.create() # -> this is the last TB, that isnt reported right now but used for future assets and passives 
        if TrialBalance.objects.order_by("id")[1] == self.id: # if it is the first created TB # cause descending order for id  ( cause maximum_id==last_id )
            self.start_saldo_credit = 0
            self.start_saldo_debit = 0
        else:
            # that mean that there is more than 1 object in queryset ( we get penultimate )
            self.start_saldo_credit = (TrialBalance.objects.order_by("id")[2]).end_saldo_credit
            self.start_saldo_debit = (TrialBalance.objects.order_by("id")[2]).end_saldo_debit

         # calc_turnover()
        dicts_of_accs, totals = get_used_accs_with_values()
        self.dicts_of_accs = str(dicts_of_accs)
        # dicts_of_accs = ast.literal_eval(self.dicts_of_accs)
        self.end_saldo_credit = self.start_saldo_credit + totals["all_credits_total"]
        self.end_saldo_debit = self.start_saldo_credit + totals["all_debits_total"]
        self.turnover_credit = totals['all_turnover_credit']
        self.turnover_debit = totals['all_turnover_debit']
        # ast.literal_eval(self.dicts_of_accs)
        self.reported = True
        # self.date_report = datetime.datetime.today() # tiemzone.now()
        self.date_report = get_simulation().today
        self.period = int(self.date_created - self.date_report)
        # self.refresh_from_db() # or not needed
        self.save() # super().save() # hz


# @receiver(pre_save, sender=TrialBalance)
# def get_period_TrialBalance(sender, instance, *args, **kwargs):
#     if instance.period == 0: # TrialBalance
#         if TrialBalance.objects.all().exists():
#             last_report = TrialBalance.objects.order_by("id").last().date_report # TODO check if its can exists()
#             instance.period = (datetime.date.today() - last_report).days # class timedelta
#         else:
#             # if there is the first instance of TrialBalance
#             instance.period = 0


# Бухгалтерский баланс
class AccountingBalance(models.Model): # каждая новая строка - новый отчет
    # start_saldo = models.IntegerField(default=0, max_length=10) # Decimal
    # turnover = models.IntegerField(default=0, max_length=10) # Decimal
    # end_saldo = models.IntegerField(default=0, max_length=10) # Decimal
    assets_total = models.FloatField(default=0.0)  # 12 dig
    passives_total = models.FloatField(default=0.0)
    reported = models.BooleanField(default=False) #  1 - that instance of AccountingBalance was reported
    date_created = MyDateField(auto_now_add=True) # right after previous reported ( so there from we can get period)
    date_report = MyDateField(editable=True, blank=True)#models.DateField(auto_now_add=True)                                # hz zachem esli editable
    period = models.IntegerField(default=0, max_length=10) # i shouldnt edit not from that class aka ""private""

    def get_assets(self):
        return self.assets.all()

    def get_passives(self):
        return self.passives.all()

    def get_report(self): #  TODO check working
        # self.assets.objects.filter()
        # Assets.objects.filter(assets__ab_id=self.id)
        self.assets_total = sum([(asset.debit_value - asset.credit_value) for asset in self.assets.all()]) # check without []
        self.passives_total = sum([(passive.debit_value - passive.credit_value) for passive in self.passives.all()])
        self.reported = True
        self.date_report = get_simulation().today # tiemzone.now()
        self.period = int(self.date_created - self.date_report)
        # self.refresh_from_db() # or not needed
        self.save() # super().save() # hz
        AccountingBalance.objects.create() # then ass and pass ad to it

# @receiver(pre_save, sender=AccountingBalance)
# def get_period_AccountingBalance(sender, instance, *args, **kwargs):
#     if instance.reported:
#         if instance.period == 0: # TrialBalance
#             if AccountingBalance.objects.all().exists():
#                 last_report = AccountingBalance.objects.order_by("id").last().date_report # TODO check if its can exists()
#                 instance.period = (datetime.date.today() - last_report).days # class timedelta
#             else:
#                 # if there is the first instance of TrialBalance
#                 instance.period = 0

#----------------------------------------------------------------------
# @receiver(pre_save, sender=OperativeAccounts)
# def pre_save_OA_receiver(sender, instance, *args, **kwargs):
#     field_names = ['assets', 'passives']
#     field_obj = None
#     for field in field_names:
#         try:
#             field_obj = instance._meta.get_field(field)
#         except FieldDoesNotExist:
#             pass

#     if field_obj is None:
#         print('There is no assets or passives field in model')
#     else:
#         field_obj
#----------------------------------------------------------------------






# accs for 1 operation per row
#D+ K-
#  в процессе  будет менятся колличество активов и пассивов (строк) из-за операций
# атомарность каждой строки

class Assets(models.Model): # Actives 
    """op_acc to OperativeAccounts
        debit_value 
        credit_value
    """
    # name_of_account = models.CharField(max_length=100)
    # debit_type = models.CharField(max_length=8) # Asset or Passive
    op_acc = models.ForeignKey(OperativeAccounts, on_delete=models.CASCADE, related_name='assets')
    ab = models.ForeignKey(AccountingBalance, on_delete=models.CASCADE, related_name='assets')
    tb = models.ForeignKey(TrialBalance, on_delete=models.CASCADE, related_name='assets')
    debit_value = models.FloatField(default=0.0, blank=True) # Decimal # only debit_value for !that! operation
    credit_value = models.FloatField(default=0.0, blank=True) # Decimal
    operative_day = MyDateField(auto_now_add=True) # чисто для вида и стат
    
@receiver(pre_save, sender=Assets)
def get_ab_Assets(sender, instance, *args, **kwargs):
    instance.ab = AccountingBalance.objects.order_by("id").last()
    instance.tb = TrialBalance.objects.order_by("id").last()


# #D- K+
class Passives(models.Model): 
    # name_of_account = models.CharField(max_length=100)
    # related_query_name  - найти определенную модель ( или тип модели в  той которая записана в ForeignKey)
    op_acc = models.ForeignKey(OperativeAccounts, on_delete=models.CASCADE, related_name='passives')#, related_query_name='passive')
    ab = models.ForeignKey(AccountingBalance, on_delete=models.CASCADE, related_name='passives')
    tb = models.ForeignKey(TrialBalance, on_delete=models.CASCADE, related_name='passives')
    debit_value = models.FloatField(default=0.0, blank=True) # Decimal
    credit_value = models.FloatField(default=0.0, blank=True) # Decimal
    operative_day = MyDateField(auto_now_add=True)

@receiver(pre_save, sender=Passives)
def get_ab_Passives(sender, instance, *args, **kwargs):
    instance.ab = AccountingBalance.objects.order_by("id").last()
    instance.tb = TrialBalance.objects.order_by("id").last()








# # every that class have own chain_of_accounting
# class Sale(models.Model):
#     from_op_account = models.ForeignKey(OperativeAccounts, on_delete=models.CASCADE, related_name='sales')
#     to_op_account = models.ForeignKey(OperativeAccounts, on_delete=models.CASCADE, related_name='sales')

#     class Meta:
#         constraints = [
#             models.CheckConstraint(
#                 check=models.Q(from_op_account__number != to_op_account__number), name='diffrent OperativeAccounts'
#             )
#         ]



# class Purchase(models.Model): # op accounts should be diffrent!!!
#     from_op_account = models.ForeignKey(OperativeAccounts, on_delete=models.CASCADE, related_name='purchases')
#     to_op_account = models.ForeignKey(OperativeAccounts, on_delete=models.CASCADE, related_name='purchases')

#     # class Meta:
#     #     constraints = [
#     #         models.CheckConstraint(
#     #             check=models.Q(from_op_account__number != to_op_account__number), name='diffrent OperativeAccounts'
#     #         )
#     #     ]