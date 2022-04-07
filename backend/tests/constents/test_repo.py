from django.test import TestCase

from constents import UserTypeChoices


class UserTypeChoicesTest(TestCase):
    def test_get_name(self):
        for key, val in UserTypeChoices.choices:
            self.assertEqual(UserTypeChoices.get_name(key), val)
        self.assertEqual(UserTypeChoices.get_name("choices"), "choices")
