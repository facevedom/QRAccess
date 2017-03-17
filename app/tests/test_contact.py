from django.test import TestCase

from app.models import EndUser
from app.models import Room
from app.models import Company
from app.models import Event
from app.models import Permission

class ContactTest(TestCase):

    def test_contact(self):
        """Tests the contact page."""
        response = self.client.get('/contact')
        self.assertTemplateUsed(response, 'app/contact.html')