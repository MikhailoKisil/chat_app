import re

from django.core.exceptions import ValidationError


def nickname_validator(nickname):
    if not re.match(r'^[A-Za-z0-9_\-]+$', nickname):
        raise ValidationError('Нікнейм повинен містити лише символи латинського алфавіту, цифри, символи підкерслення і дефіси.')
    if not re.match(r'^[A-Za-z0-9].*$', nickname):
        raise ValidationError('Нікнейм повинен починатись або на букву або на цифру.')