from django.contrib import admin
from django.conf.urls import url, include


urlpatterns = [
    url(r'^register/', register_view, name='register'),
    url(r'^login/', login_view, name='login'),
    url(r'^logout/', logout_view, name='logout'),
    url(r'^profile/(?P<slug>[\w-]+)/$', profile_view, name='profile'),
    url(r'^profile/(?P<slug>[\w-]+)/update/$', profile_update, name='update'),
    url(r'^profile/(?P<slug>[\w-]+)/delete/$', profile_delete, name='delete'),
]