from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# from accounts.models import Pharmacist, Product
# Create your models here.


# after clients purchase 
class Assessment(models.Model): # ProductAssessment -> to change vendors if bad product # PharmacistAssessment -> to change pharmacist if bad service #  --------- PromouterAssessment ( increase or decrease of sales )
    # vednor # pharmacist #
    assess = models.IntegerField(
        default=1, 
        validators=[
            MinValueValidator(1),
            MaxValueValidator(10)
        ]
        )


# class PharmacistAssessment(Assessment, ):

# class ProductAssessment(Assessment, ):