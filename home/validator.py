from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def name_validation(value, *args, **kwargs):
    if value.isalpha() == False and value == ' ':
        raise ValidationError(
            _('%(value)s is not an string'),
            params={'value': value},
        )


def phone_no_validation(value, *args, **kwargs):

    if value.isnumeric() == False or len(value) < 9:
        raise ValidationError(
            _('%(value)s is not a valid phone number'),
            params={'value': value},
        )


def mobile_no_validation(value, *args, **kwargs):
    print(value)
    print(value[0])
    print(type(value))
    if value.isnumeric() == False or len(value) < 10 or not value[0] == '9':
        raise ValidationError(
            _('%(value)s is not a valid mobile number'),
            params={'value': value},
        )