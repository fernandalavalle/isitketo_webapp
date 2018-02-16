import re


def food_name(food_name):
    """Sanitizes the food keys in the admin/edit/<food_name> path.

    Replaces unicode characters to corresponding ASCII characters. This allows unicode to be mapped
    as expected to comparable ASCII names.

    Ex: u'jalapeno\u's -> jalapenos

    Replaces characters that are not legal in file paths by GCS or Linux/Windows. Does not affect
    how food names will appear to the user.

    """
    # n tilde to n.
    cleaner = re.sub(u'\u00f1', 'n', food_name)
    # e with an accent to e.
    cleaner = re.sub(u'[\u00e8-\u00eb]', 'e', cleaner)
    # Gets rid of Unicode and ASCII apostrophes.
    cleaner = re.sub(u'\u2019', '', cleaner)
    cleaner = re.sub(r'\'', '', cleaner)
    cleaner = re.sub('&', '-and-', cleaner)
    # Get rid of ".
    cleaner = re.sub(u'[\u201c-\u201d]', '', cleaner)
    # Unicode dashes to spaces that will then become ASCII dashes below.
    cleaner = re.sub(u'[\u2010-\u2015]', ' ', cleaner)
    # Make all other symbols into -.
    cleaner = re.sub(r'[^-\d\w%\']|\s|_', '-', cleaner)
    # Collapse neighboring hyphens into one.
    cleaner = re.sub(r'-{2,}', '-', cleaner)
    # Get rid of trailing or leading symbols.
    return re.sub(r'^[^\d\w]|[^\d\w]$', '', cleaner)
