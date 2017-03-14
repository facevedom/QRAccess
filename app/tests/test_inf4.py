from django.test import TestCase

from app.forms import User_self_registration


class INF4Test(TestCase):
    """
        Tests for user story: INF5
    """
    def test_user_access_the_link_received(self):
        # tests for validation failure if user's data is empty
        form_data = {'email': '', 'id': '', 'name': '', 'last_name': '', 'event_id': ''}
        form = User_self_registration(data=form_data)
        self.assertFalse(form.is_valid())