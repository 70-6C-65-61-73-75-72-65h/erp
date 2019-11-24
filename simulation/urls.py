from django.contrib import admin
from django.conf.urls import url, include

from .views import simulation_page, simulation_create, simulate, current_simulation_info

urlpatterns = [
    url(r'^simulation_page/', simulation_page, name='simulation_page'),
    url(r'^simulation_create/', simulation_create, name='simulation_create'),
    url(r'^simulate/(?P<action>[\w]+)/', simulate, name='simulate'), # start / stop
    url(r'^simulation_refresh/', current_simulation_info, name='current_simulation_info'),
]