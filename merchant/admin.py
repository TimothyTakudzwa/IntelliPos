from django.contrib import admin

from .models import POSTerminal, MerchantProfile, BankAccount

admin.site.register(MerchantProfile)
admin.site.register(POSTerminal)
admin.site.register(BankAccount)


# Register your models here.
