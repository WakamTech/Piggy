from django.core.exceptions import ValidationError
import re

def validate_phone(value):
    pattern = r'^\+\d{11,14}$'
    if not re.match(pattern, value):
        raise ValidationError('Phone number must be in the format +22954247864, +2250102030405, etc.')
