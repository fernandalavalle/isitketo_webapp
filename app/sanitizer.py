# coding=utf-8
import re


def sanitize_food_name(food_name):
    return re.sub(r'[^a-zA-Z\-\.\s&*\+:0-9]', '', food_name)


def sanitize_food_path(food_path):
    """Sanitizes the food keys in the admin/edit/<food_name> path.

    Special handling of unicode apostrophe, &, ñ and e with an accent.
    """
    # ñ to n
    cleaner = re.sub(u'\u00f1', 'n', food_path)
    # Unicode apostrophe to apostrophe
    cleaner = re.sub(u'\u2019', '\'', cleaner)
    # e with an accent
    cleaner = re.sub(u'[\u00e8-\u00eb]', 'e', cleaner)
    cleaner = re.sub('&', '-and-', cleaner)
    # Get rid of "
    cleaner = re.sub(u'[\u201c-\u201d]', '', cleaner)
    # Dashes to dashes
    cleaner = re.sub(u'[\u2010-\u2015]', ' ', cleaner)
    # Make all other
    cleaner = re.sub(r'[^-\d\w%\']|\s|_', '-', cleaner)
    # Get rid of double hyphens
    cleaner = re.sub(r'-{2,}', '-', cleaner)
    # Get ride of trailing or leading symbols
    return re.sub(r'^[^\d\w]|[^\d\w]$', '', cleaner)
