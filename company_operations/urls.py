from django.contrib import admin
from django.conf.urls import url, include

from .views import list_of_hfcs, certain_hfc, inventory_tracking_purchase_delivery, inventory_tracking_wht_delivery

urlpatterns = [
    url(r'^it_purchases/$', inventory_tracking_purchase_delivery, name='inventory_tracking_purchase_delivery'),
    url(r'^it_whts/$', inventory_tracking_wht_delivery, name='inventory_tracking_wht_delivery'),
    url(r'^hfc/(?P<id>[\d]+)/$', certain_hfc, name='certain_hfc'),
    url(r'^hfcs/$', list_of_hfcs, name='list_of_hfcs'),
]