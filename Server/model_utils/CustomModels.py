# from django.db import models
# from django.core.validators import MaxValueValidator, MinValueValidator

from random import choice
from string import ascii_letters, digits, punctuation


def generate_random_string(length):
    chars = ascii_letters + digits + punctuation
    salt = ''.join(choice(chars) for c in range(length))
    return salt


# class CustomModel:
#     @staticmethod
#     def percentage_field(blank=False, null=False):
#         return models.FloatField(
#             default=0,
#             validators=[
#                 MinValueValidator(0),
#                 MaxValueValidator(100)
#             ],
#             blank=blank,
#             null=null
#         )
#
#     @staticmethod
#     def colorFieldRGB(blank=False, null=False):
#         return models.IntegerField(
#             default=0,
#             validators=[
#                 MinValueValidator(0),
#                 MaxValueValidator(255)
#             ],
#             blank=blank,
#             null=null
#         )