from django.core.validators import RegexValidator
import re



# Custom username validator that mimics Django's built-in 'validate_unicode_slug'
# but defines error message, error code
username_validator = RegexValidator(
    regex=r'^[\w\-]+$',       # checks username contains only Unicode letters, numbers, underscores, hyphens
    message=(
        "Oops… Your username has characters that aren't allowed. "
        "Please only use letters, numbers, hyphens (-), or underscores (_)."
    ),
    code="invalid_username",
    flags=re.UNICODE
)

