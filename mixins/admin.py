from django.contrib import admin
from .models import Address#, MyDateField - TypeError: 'type' object is not iterable
from .forms import AddressForm
from django.conf import settings

admin.ModelAdmin.list_per_page = settings.LIST_PER_PAGE
# Register your models here.
# admin.site.register(Address)
# admin.site.register(MyDateField) # TypeError: 'type' object is not iterable

# MyDateField - > models.DateField(editable=True, auto_now_add=False, auto_now=False) -> while creation - set get_simulation().today

    # address_line # street // prospect // enter there an address # first 2 elems in list after strip by ',' 
    # city
    # region
    # country
    # postal_code
    # full_address

class AdminAddressForm(admin.ModelAdmin):
	form = AddressForm

	list_display = ["address_line", "city", "region", "country", "postal_code"]
	# list_display_links = ["address_line", "city", "region", "country", "postal_code"]
	list_filter = ["address_line", "city", "region", "country", "postal_code"]

	search_fields = ["full_address"]


admin.site.register(Address, AdminAddressForm)