# coding=utf-8
import re


def sanitize_food_name(food_name):
    return re.sub(r'[^a-zA-Z\-\.\s&*\+:0-9]', '', food_name)


def sanitize_food_path(food_path):
    """Sanitizes the food keys in the admin/edit/<food_name> path.

    Allows apostrophe's, numbers, letters, &, and ñ.
    """
    no_special_char = re.sub(r'[^a-zA-Z\u00f1\'\0-9\&\u2019\]', ' ', food_path)
    return re.sub(r'[\s]', '-', food_path)
