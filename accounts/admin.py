from django.contrib import admin
from .models import Profile, Client, Worker, Vendor
from django.conf import settings

# Register your models here.
# admin.site.register(Profile)
# admin.site.register(Client)
# admin.site.register(Worker)
# admin.site.register(Vendor)

# from django.contrib import admin
# from .models import Client, Worker, Profile, Vendor
from .forms import WorkerForm, ProfileForm, VendorForm, ClientForm
admin.ModelAdmin.list_per_page = settings.LIST_PER_PAGE
# Register your models here.
class AdminClientForm(admin.ModelAdmin):
	form = ClientForm
	list_display = ["profile"]
	list_display_links = ["profile"]
	list_filter = ["profile"]

	search_fields = ["profile__user__username"]


admin.site.register(Client, AdminClientForm)

class AdminWorkerForm(admin.ModelAdmin):
	form = WorkerForm
	list_display = ["profile", "address", "kind", "salary", "birth_date", "prob_of_worker_fired", "work_on_wh", "work_on_vehicle", "work_on_dpt", "id_workon_place", "fired"]
	list_display_links = ["profile", "address"]
	list_filter = ["profile", "address", "kind", "salary", "birth_date", "prob_of_worker_fired", "work_on_wh", "work_on_vehicle", "work_on_dpt", "id_workon_place", "fired"]

	search_fields = ["profile__user__username", "kind", "fired", "id_workon_place"]


admin.site.register(Worker, AdminWorkerForm)

class AdminProfileForm(admin.ModelAdmin):
	form = ProfileForm
	list_display = ["user"]
	list_display_links = ["user"]
	list_filter = ["user"]

	search_fields = ["user__username"]

admin.site.register(Profile, AdminProfileForm)

class AdminVendorForm(admin.ModelAdmin):
	form = VendorForm
	list_display = ["profile"]
	list_display_links = ["profile"]
	list_filter = ["profile"]

	search_fields = ["profile__user__username"]


admin.site.register(Vendor, AdminVendorForm)