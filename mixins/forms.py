from django import forms

from .models import Address

class AddressForm(forms.ModelForm):
    """ called only for update """
    class Meta:
        model = Address
        fields = [
            "address_line",
            "city",
            "region",
            "country",
            "postal_code",
            "full_address"
            # address_line = models.TextField() # street // prospect // enter there an address # first 2 elems in list after strip by ',' 
            # city = models.CharField(max_length=100)
            # region = models.CharField(max_length=100)
            # country = models.CharField(max_length=100)
            # postal_code = models.CharField(max_length=100)
            # full_address
        ]
