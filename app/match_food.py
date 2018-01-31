import re

import food

_PLURAL_SUFFIX_PATTERN = re.compile(r'e?s$', flags=re.IGNORECASE)


def match(food_name):
    for fix_fn in (_remove_plural, _add_plural):
        fixed_name = fix_fn(food_name).lower()
        if food.find_by_name(fixed_name):
            return fixed_name

    return None


def _remove_plural(food_name):
    return _PLURAL_SUFFIX_PATTERN.sub('', food_name)


def _add_plural(food_name):
    food_lower = food_name.lower()
    if food_lower.endswith('ies'):
        return food_name[:-3] + 'y'
    elif food_lower.endswith('x') or food_lower.endswith('s'):
        return food_name + 'es'
    elif food_lower.endswith('y'):
        return food_name[:-1] + 'ies'
    else:
        return food_name + 's'
