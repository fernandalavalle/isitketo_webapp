import unittest

from app import food


class FoodTest(unittest.TestCase):

    def test_name_to_key(self):
        cases = (
            ('canned coconut milk', 'canned-coconut-milk'),
            (u'Raos marinara','raos-marinara'),
            (u'garlic^powder', 'garlic-powder'),
            (u'heavy_whipping_cream','heavy-whipping-cream'),
            (u'grated Parmesan','grated-parmesan'),
            (u'medium jalape\u00f1o peppers','medium-jalapeno-peppers'),
            (u'\u201cBest Low Carb\u201d tortillas','best-low-carb-tortillas'),
            (u'Cheddar-Shredded\u2013 Mild','cheddar-shredded-mild'),
            ('ghee*', 'ghee'),
            ('ghee*(coconut oil)','ghee-coconut-oil'),
            ('Dr.Pepper', 'dr-pepper'),
            ('\85%#dark#chocolate','85%-dark-chocolate'),
            ('(8oz)-Cubed-Mozzarella?','8oz-cubed-mozzarella'),
            ('Chicken Thighs, skin on','chicken-thighs-skin-on'),
            (u'Lay\u2019s^flaming@hot*cheetos@','lays-flaming-hot-cheetos'),
            ('***Delicious Brownies***', 'delicious-brownies'))  # yapf: disable
        for raw, expected in cases:
            actual = food.name_to_key(raw)
            self.assertEqual(actual.id(), expected,
                             '[%s] != [%s] (original=[%s])' % (actual, expected,
                                                               raw))
