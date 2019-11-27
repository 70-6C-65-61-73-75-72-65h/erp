from django.contrib import admin
from .models import CommunalServisePayment, SalaryPayment, Veh_repair_Payment, Purchase, PurchaseClaim, Sale, WHTransferClaim, WHTransfer, WHProduct, WareHouse, Product, Department, Fuel, Vehicle# DemandForecasting, DemandForecastingReport
# Register your models here.
admin.site.register(CommunalServisePayment)
admin.site.register(SalaryPayment)
admin.site.register(Veh_repair_Payment)
admin.site.register(Purchase)

admin.site.register(PurchaseClaim)
admin.site.register(Sale)
admin.site.register(WHTransferClaim)
admin.site.register(WHTransfer)

admin.site.register(WHProduct)
admin.site.register(WareHouse)
admin.site.register(Product)
# admin.site.register(DemandForecasting)

# admin.site.register(DemandForecastingReport)
admin.site.register(Department)
admin.site.register(Fuel)
admin.site.register(Vehicle)
