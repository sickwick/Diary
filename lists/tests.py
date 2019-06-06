from django.test import TestCase

class SmokeTest(TestCase):
    def test_math_bad(self):
        self.assertEqual(1+1, 3)