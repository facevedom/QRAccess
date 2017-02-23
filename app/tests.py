"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".
"""

import django
from django.test import TestCase
from app.utils import random_string, random_int
from app.forms import User_self_registration

# TODO: Configure your database in settings.py and sync before running tests.

class ViewTest(TestCase):
    """Tests for the application views."""

    if django.VERSION[:2] >= (1, 7):
        # Django 1.7 requires an explicit setup() when running tests in PTVS
        @classmethod
        def setUpClass(cls):
            super(ViewTest, cls).setUpClass()
            django.setup()

    def test_home(self):
        """Tests the home page."""
        response = self.client.get('/')
        self.assertContains(response, 'Home Page', 1, 200)

    def test_contact(self):
        """Tests the contact page."""
        response = self.client.get('/contact')
        self.assertContains(response, 'Contact', 3, 200)

    def test_about(self):
        """Tests the about page."""
        response = self.client.get('/about')
        self.assertContains(response, 'About', 3, 200)

    """
        Tests for EVE5
    """
    def test_user_registration_success(self):
        # tests if the POST request was succesfully received
        random_email = random_string(8) + '@domain.com'
        random_id = random_int()
        response = self.client.post('/user/registration', {'email': random_email,
                                                        'id': random_id,
                                                        'name': 'Peter',
                                                        'last_name': 'Retep',
                                                        'event_id': 'RutaN_0045HACK'
                                                        })
        self.assertContains(response, 'Congratulations', 1, 200)

    def test_user_registration_empty(self):
        # tests for validation failure if user's data is empty
        form_data = {'email': '', 'id': '', 'name': '', 'last_name': '', 'event_id': ''}
        form = User_self_registration(data=form_data)
        self.assertFalse(form.is_valid())

    def test_valid_event_id(self):
        # tests for validation failure if id is invalid
        return True
