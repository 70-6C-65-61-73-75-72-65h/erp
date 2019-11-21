from django.contrib import admin
from django.conf.urls import url, include

from .views import get_accounting_balance, get_trial_balance, perform_operations, accounting_main_page

urlpatterns = [
    url(r'^accounting_main_page/', accounting_main_page, name='accounting_main_page'),
    url(r'^accounting_balance/', get_accounting_balance, name='accounting_balance'),
    url(r'^trial_balance/', get_trial_balance, name='trial_balance'),
    url(r'^perform_operations/', perform_operations, name='perform_operations'),
]