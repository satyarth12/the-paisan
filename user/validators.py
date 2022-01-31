from django.core.validators import validate_email
from django.core.exceptions import ValidationError

def email_validator(value):
    try:
        validate_email(value)
        return True

    except ValidationError:
        return False
