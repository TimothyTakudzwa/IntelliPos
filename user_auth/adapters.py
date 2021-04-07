from django import forms
from allauth.account.adapter import DefaultAccountAdapter


class UserAccountAdapter(DefaultAccountAdapter):

    def save_user(self, request, user, form, commit=True):
        """
        Saves a new `User` instance using information provided in the
        signup form.
        """
    
        user = super().save_user(request, user, form, False)
        user.is_merchant_admin = True
        user.save()
        return user