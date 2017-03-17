from django.test import TestCase

from app.models import Permission
from app.models import EndUser
from app.models import Room
from app.models import Company
from app.models import Event

from datetime import datetime
from datetime import timedelta


class AccessTest(TestCase):

    def test_login_required_on_GET(self):
        response = self.client.get('/create/event')
        # assert redirection
        self.assertEqual(response.status_code, 302)
