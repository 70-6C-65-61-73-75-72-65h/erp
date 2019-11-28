from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# from accounts.models import Pharmacist, Product
# Create your models here.


# after clients purchase 
class Assessment(models.Model): # ProductAssessment -> to change vendors if bad product # PharmacistAssessment -> to change pharmacist if bad service #  --------- PromouterAssessment ( increase or decrease of sales )
    # vednor # pharmacist #
    # assess = models.IntegerField(
    #     default=1, 
    #     validators=[
    #         MinValueValidator(1),
    #         MaxValueValidator(10)
    #     ]
    #     )
    assess = models.IntegerField() # 1- 5
    pharmacy = models.ForeignKey('company_operations.WareHouse', related_name='assesments', on_delete=models.SET_NULL, null=True)
    worker = models.ForeignKey('accounts.Worker', related_name='assesments', on_delete=models.SET_NULL, null=True)
    client = models.ForeignKey('accounts.Client', related_name='assesments', on_delete=models.SET_NULL, null=True)
    created = models.DateField() # get_simulation().today




# class PharmacistAssessment(Assessment, ):

# class ProductAssessment(Assessment, ):