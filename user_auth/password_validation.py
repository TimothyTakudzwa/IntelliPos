from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _


class DigitValidator:
    def validate(self, password, user=None):
       if not any(char.isdigit() for char in password):
            raise ValidationError(
                _("Your Password should have at least one numeral."),
                code='password_is_weak',
            )


class UpperCaseValidator:
    def validate(self, password, user=None):
        if not any(char.isupper() for char in password):
            raise ValidationError(
                _("Your Password should contain at least one uppercase letter."),
                code='password_is_weak',
            )

    def get_help_text(self):
        return _("")


class LowerCaseValidator:
    def validate(self, password, user=None):
        if not any(char.islower() for char in password):
            raise ValidationError(
                _("Your Password should contain at least one lowercase letter."),
                code='password_is_weak',
            )

    def get_help_text(self):
        return _("")


class SpecialCharacterValidator:
    def validate(self, password, user=None):
        if not any(c for c in password if not c.isalnum() and not c.isspace()):
            raise ValidationError(
                _("Your Password should contain at least one special character."),
                code='password_is_weak',
            )

    def get_help_text(self):
        return _("")