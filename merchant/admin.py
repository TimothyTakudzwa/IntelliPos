from django.contrib import admin

from .models import Transaction, POSTerminal, MerchantProfile, BankAccount

admin.site.register(MerchantProfile)
admin.site.register(POSTerminal)
admin.site.register(Transaction)
admin.site.register(BankAccount)


# Register your models here.
