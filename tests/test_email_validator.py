import unittest

from app import email_validator


class EmailValidatorTest(unittest.TestCase):

    def test_accepts_valid_emails(self):
        valid_emails = [
            'a@b.com',
            'john.smith@gmail.com',
            'johnsmith83430@gmail.com',
            'jane-doe+isitketo@yahoo.com',
            'jane@mail4.customdomain.com',
        ]
        for email in valid_emails:
            actual = email_validator.validate(email)
            self.assertTrue(actual, '%s should be valid, got: %s' % (email,
                                                                     actual))

    def test_rejects_invalid_emails(self):
        valid_emails = [
            'Steve',
            '@',
            'john@',
            '@gmail.com',
            'john.smith@',
        ]
        for email in valid_emails:
            actual = email_validator.validate(email)
            self.assertFalse(actual, '%s should be invalid, got: %s' % (email,
                                                                        actual))
