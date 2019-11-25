from django.contrib import admin
from .models import Address#, MyDateField - TypeError: 'type' object is not iterable
# Register your models here.
admin.site.register(Address)
# admin.site.register(MyDateField) # TypeError: 'type' object is not iterable

# MyDateField - > models.DateField(editable=True, auto_now_add=False, auto_now=False) -> while creation - set get_simulation().today