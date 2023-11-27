from django.contrib import admin

# Register your models here.
from payment.models import Charges

admin.site.register(Charges)
