"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase

from accounts.models import User

class SimpleTest(TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)
    
class AssertUsers(TestCase):
    def test_initial_users(self):
        """
        Tests that returns the Users which are created from migrations
        """
        self.assertQuerysetEqual(
        	User.objects.all(),
        	['<User: admin@admin.com>', '<User: usuario@econet.com>']
    	)

