import unittest

from app import sanitizer


class ParsePathTest(unittest.TestCase):

    def test_parse_food_name_path(self):
        cases = (('canned coconut milk',
                  'canned-coconut-milk'), (u'Rao\u2019s marinara',
                                           'Rao\'s-marinara'),
                 (u'garlic^powder', 'garlic-powder'), (u'heavy_whipping_cream',
                                                       'heavy-whipping-cream'),
                 (u'grated Parmesan',
                  'grated-Parmesan'), (u'medium jalape\u00f1o peppers',
                                       'medium-jalapeno-peppers'),
                 (u'\u201cBest Low Carb\u201d tortillas',
                  'Best-Low-Carb-tortillas'), (u'Cheddar-Shredded\u2013 Mild',
                                               'Cheddar-Shredded-Mild'),
                 ('ghee*', 'ghee'), ('ghee*(coconut oil)', 'ghee-coconut-oil'),
                 ('Dr.Pepper', 'Dr-Pepper'), ('\85%#dark#chocolate',
                                              '85%-dark-chocolate'),
                 ('(8oz)-Cubed-Mozzarella?',
                  '8oz-Cubed-Mozzarella'), ('Chicken Thighs, skin on',
                                            'Chicken-Thighs-skin-on'),
                 (u'Lay\u2019s^flaming@hot*cheetos@',
                  'Lay\'s-flaming-hot-cheetos'))
        for raw, expected in cases:
            actual = sanitizer.sanitize_food_path(raw)
            self.assertEqual(actual, expected, '[%s] != [%s] (original=[%s])' %
                             (actual, expected, raw))
