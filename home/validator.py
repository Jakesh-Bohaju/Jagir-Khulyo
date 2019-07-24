from datetime import date

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def name_validation(value, *args, **kwargs):
    if value.isalpha() == False and value == ' ':
        raise ValidationError(
            _('%(value)s is not valid name.'),
            params={'value': value},
        )


def phone_no_validation(value, *args, **kwargs):
    if value.isnumeric() == False or len(value) < 9:
        raise ValidationError(
            _('%(value)s is not a valid phone number.'),
            params={'value': value},
        )


def mobile_no_validation(value, *args, **kwargs):
    if value.isnumeric() == False or len(value) < 10 or not value[0] == '9':
        raise ValidationError(
            _('%(value)s is not a valid mobile number.'),
            params={'value': value},
        )


def registration_date_validation(value, *args, **kwargs):
    today = date.today()
    if value > today:
        raise ValidationError(
            _('%(value)s is not valid date.'),
            params={'value': value},
        )


def date_of_birth_validation(value, *args, **kwargs):
    today = date.today()
    entered_age = 365 * (today.year - value.year) + 30 * (today.month - value.month) + (today.day - value.day)
    valid_age = 16 * 365
    if entered_age < valid_age or value > today:
        raise ValidationError(
            _('You must be 16 years.'),
            params={'value': value},
        )


def deadline_validation(value, *args, **kwargs):
    today = date.today()
    deadline_month = 30 * (value.month - today.month) + (value.day - today.day)
    if deadline_month > 30 or value < today:
        raise ValidationError(
            _('Maximum deadline must be 30 days'),
            params={'value': value},
        )