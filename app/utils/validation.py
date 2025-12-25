import re

EMAIL_REGEX = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"

def is_valid_email(email: str) -> bool:
    if not email:
        return False
    return re.match(EMAIL_REGEX, email) is not None
