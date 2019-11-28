from django.contrib import admin
from django.conf.urls import url, include

from .views import get_accounting_balance, get_trial_balance, accounting_main_page, list_of_abs, list_of_tbs, certain_tb, certain_ab

urlpatterns = [
    url(r'^accounting_main_page/$', accounting_main_page, name='accounting_main_page'),
    url(r'^accounting_balance/$', get_accounting_balance, name='accounting_balance'),
    url(r'^trial_balance/$', get_trial_balance, name='trial_balance'),
    url(r'^list_of_abs/$', list_of_abs, name='list_of_abs'),
    url(r'^list_of_tbs/$', list_of_tbs, name='list_of_tbs'),
    url(r'^trial_balance/(?P<id>[\d]+)/$', certain_tb, name='certain_tb'),
    url(r'^accounting_balance/(?P<id>[\d]+)/$', certain_ab, name='certain_ab'),
    # url(r'^perform_operations/', perform_operations, name='perform_operations'),
]