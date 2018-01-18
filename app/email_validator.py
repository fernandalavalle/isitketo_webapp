import re

# Deliberately permissive regex because we'd rather not filter out good
# addresses.
_VALIDATION_REGEX = re.compile(r'[^@]+@[^@]+\.[^@]+')


def validate(email):
    if not email:
        return False
    return _VALIDATION_REGEX.match(email) is not None
