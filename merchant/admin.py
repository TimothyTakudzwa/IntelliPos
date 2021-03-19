from django.contrib import admin

from .models import Transaction, User, IntelliPos, Merchant, Account, JWTToken

admin.site.register(Merchant)
admin.site.register(User)
admin.site.register(IntelliPos)
admin.site.register(Transaction)
admin.site.register(Account)

admin.site.register(JWTToken)
# Register your models here.
