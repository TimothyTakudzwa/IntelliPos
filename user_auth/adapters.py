from django import forms
from allauth.account.adapter import DefaultAccountAdapter


class UserAccountAdapter(DefaultAccountAdapter):

    def save_user(self, request, user, form, commit=True):
        """
        Saves a new `User` instance using information provided in the
        signup form.
        """
        from allauth.account.utils import user_field
        is_merchant_admin = request.data.get('is_merchant_admin', '')

        user = super().save_user(request, user, form, False)
        user_field(user, 'is_merchant_admin', request.data.get('is_merchant_admin', ''))
        user.save()
        return user