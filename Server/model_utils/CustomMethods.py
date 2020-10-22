# from django.db import models
# from django.core.validators import MaxValueValidator, MinValueValidator

from random import choice
from string import ascii_letters, digits, punctuation
from re import match as regex_match

from .PrivateMethods import ALL_CTRL_ALLOWED, ALLOWED_CTRL_DATAFILE


def generate_random_string(length):
    chars = ascii_letters + digits + punctuation
    salt = ''.join(choice(chars) for c in range(length))
    return salt


def load_allowed_controllers():
    # Loads Allowed Ip's (From controllers, added later to ALLOWED_HOSTS in settings)

    ip_pattern = "^((25[0-5]|(2[0-4]|1[0-9]|[1-9]|)[0-9])(\.(?!$)|$)){4}$"
    controllers = []

    with open(ALLOWED_CTRL_DATAFILE, 'r') as file:
        for line in file.readlines():
            reg_line = regex_match(ip_pattern, line)
            if bool(reg_line):
                controllers.append(reg_line.group())

    if controllers:
        ALL_CTRL_ALLOWED.extend(controllers)
        return True

    return False
