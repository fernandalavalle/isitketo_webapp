import re


def validate(email):
    if not email:
        return False
    return re.match(
        r'\A(?P<name>[\w\-_]+)@(?P<domain>[\w\-_]+)\.(?P<toplevel>[\w]+)\Z',
        email, re.IGNORECASE)
