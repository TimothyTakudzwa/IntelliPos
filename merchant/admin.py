from django.contrib import admin

from .models import Transaction, User, IntelliPos, MerchantProfile, BankAccount

admin.site.register(MerchantProfile)
admin.site.register(User)
admin.site.register(IntelliPos)
admin.site.register(Transaction)
admin.site.register(BankAccount)


# Register your models here.
