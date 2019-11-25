from django.contrib import admin
from .models import Profile, Client, Worker, Vendor
# Register your models here.
admin.site.register(Profile)
admin.site.register(Client)
admin.site.register(Worker)
admin.site.register(Vendor)