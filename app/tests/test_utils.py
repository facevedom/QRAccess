from django.test import TestCase
from app.utils import random_int
from app.utils import random_string


class UtilsTest(TestCase):
    """
        Tests for utils
    """
    def test_random_string(self):
        # tests the random string generator function
        length = 23
        random_text = random_string(23)
        self.assertTrue(isinstance(random_text, str))
        self.assertEquals(len(random_text), length)

    def test_utils_random_int(self):
        # tests the random integer generator function
        min = 23
        max = 98457
        random_number = random_int(min, max)
        self.assertGreaterEqual(random_number, min)
        self.assertLessEqual(random_number, max)

        random_number = random_int()
        self.assertGreaterEqual(random_number, 0)
        self.assertLessEqual(random_number, 9999999999)

        self.assertTrue(isinstance(random_number, int))