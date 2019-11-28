from django.contrib import admin
from django.conf.urls import url, include

from .views import simulation_page, simulation_create, simulate, current_simulation_info, simulation_auto_create, simulation_model_inner_data

urlpatterns = [
    url(r'^simulation_page/', simulation_page, name='simulation_page'),
    url(r'^simulation_create/', simulation_create, name='simulation_create'),
    url(r'^simulation_auto_create/', simulation_auto_create, name='simulation_auto_create'),
    url(r'^simulate/(?P<action>[\w]+)/', simulate, name='simulate'), # start / stop
    url(r'^simulation_refresh/', current_simulation_info, name='current_simulation_info'),
    url(r'^simulation_data/', simulation_model_inner_data, name='simulation_data'),
]