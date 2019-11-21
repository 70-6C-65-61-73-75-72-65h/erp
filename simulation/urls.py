from django.contrib import admin
from django.conf.urls import url, include

from .views import simulation_page, simulation_create, simulation#, current_simulation_info

urlpatterns = [
    url(r'^simulation_page/', simulation_page, name='simulation_page'),
    url(r'^simulation_create/', simulation_create, name='simulation_create'),
    url(r'^simulation/', simulation, name='simulation'),
    # url(r'^accounting_balance/', get_accounting_balance, name='accounting_balance'),
    # url(r'^trial_balance/', get_trial_balance, name='trial_balance'),
    # url(r'^perform_operations/', perform_operations, name='perform_operations'),
]