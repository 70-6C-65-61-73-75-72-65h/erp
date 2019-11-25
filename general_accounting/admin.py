from django.contrib import admin
from .models import OperativeAccounts, TrialBalance, AccountingBalance, Assets, Passives, TaxRate
# Register your models here.
admin.site.register(OperativeAccounts)
admin.site.register(TrialBalance)
admin.site.register(AccountingBalance)
admin.site.register(Assets)
admin.site.register(Passives)
admin.site.register(TaxRate)